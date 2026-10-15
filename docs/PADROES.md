# 📐 Padrões para manter o GitHub organizado

Regras curtas para seguir daqui pra frente, para que a bagunça não volte.

## 1. Um projeto = um repositório (não um repositório por ajuste)

A maior fonte de bagunça hoje são repositórios como `fim`, `att`, `CORRECAO`,
`ultimo_ajuste` e `Fluxo-Royale-Frontend2.1`: cada ajuste ou versão virou um
repositório novo. O Git já resolve isso dentro do mesmo repositório:

| Em vez de… | Faça |
|---|---|
| Criar `projeto-correcao` para testar um ajuste | Crie um **branch**: `git switch -c ajuste-relatorio`, teste e depois faça merge na `main` |
| Criar `Homolog-projeto` para homologação | Use um branch `homolog`. A Vercel cria uma **URL de preview** para cada branch automaticamente |
| Criar `projeto2.1`, `projeto5.0` | Marque a versão com uma **tag** e publique uma **Release**: `git tag v5.0.0 && git push --tags` |
| Copiar a pasta para "garantir" | O histórico já guarda tudo. Para voltar a um ponto: `git switch -c resgate <commit>` |

## 2. Nome do repositório

- `kebab-case`, tudo minúsculo, sem acento: `summer-drinks-atendimento`
- Projetos com duas partes: `<projeto>-frontend` e `<projeto>-backend`
- Sem versão no nome (`2.1`, `5.0`, `final`, `novo`) — versão é tag
- Nome do app e do repositório iguais (ex.: o app CLO está no repo `COL-Front`)

## 3. Descrição (o "About" do repositório)

Uma frase: **o que é + para quem + stack principal**. Até ~120 caracteres
aparece inteira nos cards.

> ✅ `PWA de cardápio e pedidos da Gringo Pizzaria, integrado à Anota AI.`
> ❌ `projeto pizzaria` · ❌ vazio

Coloque também o link do site publicado no campo **Website**.

## 4. Tópicos

Entre 5 e 10, em minúsculas com hífen. Use sempre nesta ordem de prioridade:

1. **Linguagem**: `typescript`, `javascript`, `python`, `csharp`
2. **Framework**: `react`, `nextjs`, `vite`, `express`, `react-native`
3. **Dados/infra**: `postgresql`, `supabase`, `prisma`, `sqlite`, `docker`, `vercel`
4. **Domínio**: `erp`, `pdv`, `delivery`, `cardapio-digital`, `automation`, `streaming`
5. **Estado**: `prototype` para protótipos

## 5. README mínimo

Todo repositório público precisa de, no mínimo:

1. Nome e uma frase do que é
2. **Um print** da tela principal (é o que mais chama atenção)
3. Link da demo, se houver
4. Tecnologias
5. Como rodar localmente

Use o modelo [`modelos/README-projeto.md`](../modelos/README-projeto.md).
Apague o README padrão do Lovable ("Welcome to your Lovable project").

## 6. Commits

Mensagens no formato `tipo: o que mudou`, no imperativo:

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | funcionalidade nova | `feat: adiciona filtro por setor nas requisições` |
| `fix` | correção | `fix: corrige cálculo de estoque mínimo` |
| `docs` | só documentação | `docs: adiciona print ao README` |
| `refactor` | reorganização sem mudar comportamento | `refactor: separa StockTable em componentes` |
| `chore` | dependências, configuração | `chore: atualiza vite para 6.x` |

Evite `ajuste`, `att`, `final`, `agora vai`: daqui a 3 meses ninguém sabe o que foi.

## 7. Segredos

- `.env` **sempre** no `.gitignore`; versione só o `.env.example` com valores falsos
- Confira se **Secret scanning** e **Push protection** estão ligados (grátis em
  repositórios públicos), na seção de segurança do *Settings* de cada repositório.
  Com eles, o GitHub bloqueia o push se detectar uma chave
- Se uma chave real vazar, **troque a chave**. Apagar o commit não basta

## 8. Ciclo de vida de um repositório

| Situação | O que fazer |
|---|---|
| Projeto ativo e apresentável | Público, descrição, tópicos, README com print |
| Ativo, mas de cliente ou com dados sensíveis | Privado |
| Terminou ou foi substituído | **Arquivar** (somente leitura, reversível) |
| Versão antiga que confunde quem visita | Privar **e** arquivar |
| Vazio ou cópia idêntica de outro | Excluir, depois de conferir |

## 9. Vitrine do perfil

- **6 fixados** (*Customize your pins* no perfil): os projetos mais completos,
  com demo e README. Hoje: Fluxo Royale, Olwe, ClipPro, Ótica Digital Look,
  Gringo Pizzaria e CLO
- Atualize o README de perfil (`Corrar/Corrar`) quando um projeto novo entrar
  nos destaques

## 10. Revisão mensal (10 minutos)

- [ ] Algum repositório novo sem descrição ou tópicos?
- [ ] Algum repositório criado só para um ajuste? → vire branch e arquive
- [ ] Os fixados ainda são os 6 melhores?
- [ ] Algum PR do Dependabot esperando?
- [ ] Rodar `python organizar/organizar.py` para conferir o plano
