#!/usr/bin/env python3
"""Aplica o plano de organização de repos.json usando o GitHub CLI (gh).

Por padrão só SIMULA: mostra cada comando que rodaria e não muda nada.

    python organizar.py                        # simulação de tudo
    python organizar.py --aplicar              # descrições, tópicos, privar e arquivar
    python organizar.py --aplicar --renomear   # + renomeia para o padrão kebab-case
    python organizar.py --aplicar --excluir    # + exclui (pede o nome digitado, repo a repo)
    python organizar.py --so ClipPro Olwe-Studio

Requisitos: Python 3.8+ e o gh autenticado (gh auth login).
Para excluir, o token precisa do escopo delete_repo:
    gh auth refresh -h github.com -s delete_repo
"""

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

TOPICO = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
NOME_REPO = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def validar(plano):
    erros = []
    vistos = set()
    for r in plano["repos"]:
        nome = r.get("nome") or "?"
        if nome in vistos:
            erros.append(f"{nome}: aparece mais de uma vez")
        vistos.add(nome)
        desc = r.get("descricao")
        if desc is not None and len(desc) > 350:
            erros.append(f"{nome}: descrição com {len(desc)} caracteres (máximo 350)")
        topicos = r.get("topicos") or []
        if len(topicos) > 20:
            erros.append(f"{nome}: {len(topicos)} tópicos (máximo 20)")
        for t in topicos:
            if not TOPICO.match(t):
                erros.append(f"{nome}: tópico inválido '{t}' (minúsculas, números e hífen; até 50)")
        novo = r.get("novo_nome")
        if novo and not NOME_REPO.match(novo):
            erros.append(f"{nome}: novo_nome inválido '{novo}'")
    return erros


def passos(r, dono, atual, estado, renomear, excluir):
    """Lista de (rótulo, argumentos do gh) para levar o repo ao estado do plano."""
    alvo = f"{dono}/{atual}"
    if r.get("excluir"):
        return [("excluir", ["repo", "delete", alvo, "--yes"])] if excluir else []

    # Repo arquivado é somente leitura: não aceita mais edição nem renomeação.
    if estado.get("arquivado"):
        return []

    edicao = []
    if r.get("descricao") is not None:
        edicao += ["--description", r["descricao"]]
    if r.get("site") is not None:
        edicao += ["--homepage", r["site"]]
    if r.get("topicos"):
        edicao += ["--add-topic", ",".join(r["topicos"])]

    lista = []
    if edicao:
        lista.append(("editar", ["repo", "edit", alvo, *edicao]))
    if r.get("privar") and estado.get("visibilidade") != "PRIVATE":
        lista.append(("privar", ["repo", "edit", alvo, "--visibility", "private",
                                 "--accept-visibility-change-consequences"]))
    novo = r.get("novo_nome")
    if renomear and novo and novo != atual:
        lista.append(("renomear", ["repo", "rename", novo, "--repo", alvo, "--yes"]))
        alvo = f"{dono}/{novo}"
    if r.get("arquivar"):
        lista.append(("arquivar", ["repo", "archive", alvo, "--yes"]))
    return lista


def rodar_gh(gh, args):
    proc = subprocess.run([gh, *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def ler_estado(gh, dono, nome):
    """Estado atual no GitHub. O GitHub redireciona nomes antigos após renomear."""
    codigo, saida = rodar_gh(gh, ["repo", "view", f"{dono}/{nome}",
                                  "--json", "name,isArchived,visibility"])
    if codigo != 0:
        return None
    dados = json.loads(saida)
    return {"nome": dados["name"], "arquivado": dados["isArchived"],
            "visibilidade": dados["visibility"]}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Organiza os repositórios conforme repos.json.")
    ap.add_argument("--arquivo", default=str(Path(__file__).with_name("repos.json")))
    ap.add_argument("--aplicar", action="store_true", help="executa de verdade (sem isso, só simula)")
    ap.add_argument("--renomear", action="store_true", help="inclui as renomeações (novo_nome)")
    ap.add_argument("--excluir", action="store_true", help="inclui as exclusões, com confirmação digitada")
    ap.add_argument("--so", nargs="+", metavar="REPO", help="limita a estes repositórios")
    args = ap.parse_args()

    plano = json.loads(Path(args.arquivo).read_text(encoding="utf-8"))
    dono = plano["dono"]
    erros = validar(plano)
    if erros:
        print("Corrija o repos.json antes de continuar:")
        for e in erros:
            print(f"  - {e}")
        return 2

    repos = plano["repos"]
    if args.so:
        desconhecidos = set(args.so) - {r["nome"] for r in repos}
        if desconhecidos:
            print(f"Não estão no repos.json: {', '.join(sorted(desconhecidos))}")
            return 2
        repos = [r for r in repos if r["nome"] in args.so]

    gh = None
    if args.aplicar:
        gh = shutil.which("gh")
        if not gh:
            print("GitHub CLI (gh) não encontrado. Instale: https://cli.github.com")
            return 2
        codigo, saida = rodar_gh(gh, ["auth", "status"])
        if codigo != 0:
            print("O gh não está autenticado. Rode: gh auth login")
            print(saida)
            return 2

    print(f"Modo: {'APLICAR' if args.aplicar else 'SIMULAÇÃO (nada será alterado)'}")
    print(f"Conta: {dono} | Repositórios no plano: {len(repos)}\n")

    feitos = falhas = pulados = 0
    exclusoes_pendentes = []
    for r in repos:
        nome = r["nome"]
        if r.get("excluir") and not args.excluir:
            exclusoes_pendentes.append(nome)
            continue

        estado = {}
        atual = nome
        if args.aplicar:
            estado = ler_estado(gh, dono, nome)
            if estado is None:
                print(f"[{nome}] não encontrado (já excluído ou sem acesso) — pulando")
                pulados += 1
                continue
            atual = estado["nome"]

        lista = passos(r, dono, atual, estado, args.renomear, args.excluir)
        if not lista:
            motivo = "já arquivado" if estado.get("arquivado") else "nada a fazer"
            print(f"[{nome}] {motivo}")
            continue

        print(f"[{nome}] ({r.get('categoria', '')})")
        for rotulo, gh_args in lista:
            linha = "gh " + shlex.join(gh_args)
            if not args.aplicar:
                print(f"    {rotulo:<9} {linha}")
                continue
            if rotulo == "excluir":
                resposta = input(f"    Excluir {dono}/{atual} para sempre? Digite o nome para confirmar: ")
                if resposta.strip() != atual:
                    print("    exclusão cancelada")
                    pulados += 1
                    continue
            codigo, saida = rodar_gh(gh, gh_args)
            if codigo == 0:
                feitos += 1
                print(f"    ok        {rotulo}")
            else:
                falhas += 1
                print(f"    FALHOU    {rotulo}: {saida}")
                if rotulo == "excluir" and "delete_repo" in saida:
                    print("              rode: gh auth refresh -h github.com -s delete_repo")
                break  # não segue para os próximos passos deste repo
        print()

    if exclusoes_pendentes:
        print("Marcados para excluir (rode com --excluir para tratar um a um):")
        print("  " + ", ".join(exclusoes_pendentes) + "\n")
    if args.aplicar:
        print(f"Concluído: {feitos} alterações, {falhas} falhas, {pulados} pulados.")
    else:
        print("Nada foi alterado. Revise o repos.json e rode de novo com --aplicar.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
