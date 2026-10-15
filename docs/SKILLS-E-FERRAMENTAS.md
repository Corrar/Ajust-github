# 🧰 Skills e ferramentas para otimizar o GitHub

## Plugins do Claude (catálogo de plugins do claude.ai)

Encontrados no catálogo e úteis para o seu caso. Nenhum vem instalado; dá para
ativar pelo card de instalação na conversa ou pelo catálogo de plugins.

| Plugin | O que faz | Quando usar |
|---|---|---|
| **GitHub Portfolio Builder** | Analisa um perfil ou repositório como portfólio e devolve até 5 melhorias priorizadas, com link para a evidência | Depois de aplicar este plano, para uma segunda opinião sobre o perfil |
| **Make Documentation** | Gera e atualiza README.md e a pasta `/docs` de um projeto direto nos arquivos | Para os repositórios sem README (SummerDrinks_Atendimento, DashProject-Frontend, Hub-Academico, garcas-burguer) |
| **CI Optimizer** | Revisa GitHub Actions: cache faltando, execuções desperdiçadas, timeouts, Actions sem versão fixa | Para o `ci.yml` do Fluxo-Royale-Backend e futuros workflows |
| **GitHub** (oficial) | Servidor MCP oficial do GitHub: issues, PRs, revisão de código e busca | Para gerenciar issues e PRs pelo Claude Code |
| **GitKraken** | Dá ao Claude o contexto real de commits, branches, PRs e issues de todos os seus repositórios | Para perguntar "o que mudou no Fluxo este mês?" |

## Recursos do próprio GitHub (grátis)

| Recurso | Onde | Para quê |
|---|---|---|
| **README de perfil** | Repositório público com o nome do usuário (`Corrar/Corrar`) | A "capa" do perfil. Modelo pronto em [`perfil/`](../perfil/README.md) |
| **Fixados** | Perfil → *Customize your pins* | Mostra os 6 melhores projetos no topo |
| **Repositório `.github`** | Repositório público chamado `.github` | Modelos de issue e PR padrão para **todos** os repositórios. Modelo pronto em [`modelos/dot-github/`](../modelos/dot-github) |
| **Social preview** | Repo → *Settings → General → Social preview* | Imagem de 1280×640 que aparece quando o link é compartilhado no WhatsApp/LinkedIn |
| **Releases e tags** | Repo → *Releases* | Marcar versões (`v5.0.0`) em vez de criar repositórios novos |
| **Projects** | Perfil → *Projects* | Quadro Kanban para planejar tarefas de vários repositórios |
| **Dependabot** | `.github/dependabot.yml` | PRs automáticos de atualização. Modelo em [`modelos/dependabot.yml`](../modelos/dependabot.yml) |
| **Secret scanning + Push protection** | Repo → *Settings*, seção de segurança | Bloqueia push com chaves e senhas |

## Ferramentas para o README de perfil

| Ferramenta | Uso no seu perfil | Observação |
|---|---|---|
| [shields.io](https://shields.io) | Badges (LinkedIn, e-mail, demo, status) | Muito estável |
| [skillicons.dev](https://skillicons.dev) | Ícones das tecnologias | Lista de ícones disponíveis no site |
| [`perfil/scripts/gerar_cards.py`](../perfil/scripts/gerar_cards.py) (deste kit) | Cards estilo terminal: `whoami` com o logo em ASCII, analytics com sequências e mapa de contribuições | Roda na sua própria Action com os seus dados; temas verde e rosa |
| [Platane/snk](https://github.com/Platane/snk) | Cobrinha comendo o gráfico de contribuições | Gerada pela sua própria Action, sem depender de servidor de terceiros |
| [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | Cards de estatísticas e linguagens | A instância pública é "best effort" e cai por limite de uso ([discussão](https://github.com/anuraghazra/github-readme-stats/issues/4748)). Se quiser usar, hospede a sua cópia na Vercel |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | Infográficos completos (linguagens, atividade, conquistas) | Roda via Actions; precisa de um token pessoal como secret |

## Linha de comando

- **[GitHub CLI (`gh`)](https://cli.github.com)** — é ele que o script
  [`organizar/organizar.py`](../organizar/organizar.py) usa. Comandos úteis:
  - `gh repo list Corrar --limit 100` — lista tudo
  - `gh repo edit Corrar/<repo> --description "..." --add-topic react,typescript`
  - `gh repo archive Corrar/<repo>`
  - `gh release create v1.0.0 --generate-notes` — cria uma release com as notas geradas dos commits
