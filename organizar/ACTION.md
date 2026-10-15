# 📱 Organizar pelo celular

A Action **Organizar repositórios** roda o [`organizar.py`](organizar.py) nos
servidores do GitHub. Funciona pelo navegador do celular ou pelo app do GitHub.

## 1. Simular (não precisa de token)

1. Abra **github.com/Corrar/Ajust-github/actions**
2. Toque em **Organizar repositórios** → **Run workflow**
3. Deixe `modo` = **simular** e toque em **Run workflow**
4. Abra a execução: o **resumo** mostra cada mudança que seria feita

Se quiser mudar algo, edite o [`repos.json`](repos.json) (dá para editar pelo
próprio site: abra o arquivo e toque no lápis) e simule de novo.

## 2. Criar o token (uma vez)

O token padrão das Actions não pode mexer em outros repositórios, então a Action
usa um token seu, guardado como secret.

1. Abra **github.com/settings/personal-access-tokens/new**
2. Preencha:
   - **Token name**: `organizar`
   - **Expiration**: 7 dias
   - **Repository access**: *All repositories*
   - **Permissions → Repositories → Administration**: *Read and write*
3. Toque em **Generate token** e copie o token (ele só aparece uma vez)
4. Abra **github.com/Corrar/Ajust-github/settings/secrets/actions/new**
5. **Name**: `ORGANIZAR_TOKEN` · **Secret**: cole o token → **Add secret**

## 3. Aplicar

1. **Actions** → **Organizar repositórios** → **Run workflow**
2. `modo` = **aplicar** (deixe `renomear` desmarcado na primeira vez)
3. O resumo mostra `ok` ou `FALHOU` em cada passo. Pode rodar de novo sem
   problema: o script pula o que já foi arquivado ou renomeado.

Opcional: rode de novo com **renomear** marcado para padronizar os nomes.
Depois de renomear, atualize os clones no computador:
`git remote set-url origin https://github.com/Corrar/<novo-nome>.git`.

## 4. Depois

- **Apague o token**: github.com/settings/personal-access-tokens → `organizar` → *Delete*.
  Ele dá acesso de administrador aos seus repositórios.
- **Repositórios vazios** (`Fluxo`, `GringoPizzaria-Back`, `novo_ajuste`): a
  Action não exclui nada. Para excluir, abra cada um → *Settings* → *Danger Zone*
  → *Delete this repository*.
