# 🔎 Auditoria do GitHub — Corrar

> Levantamento feito em **15/10/2026** sobre os **63 repositórios** da conta
> (37 públicos, 26 privados). O plano completo, repo a repo, está em
> [`organizar/repos.json`](../organizar/repos.json) e é aplicado pelo script
> [`organizar/organizar.py`](../organizar/organizar.py).

## Diagnóstico

| Ponto | Situação encontrada |
|---|---|
| **Perfil** | Não existe README de perfil (o repositório `Corrar/Corrar`). Quem visita vê só a lista de repositórios. |
| **Descrições** | Só **2 de 63** repositórios têm descrição. |
| **Tópicos** | Só **1 de 63** tem tópicos (`COL-Front`). Sem tópicos, os projetos não aparecem nas buscas do GitHub. |
| **Fixados** | Nenhum projeto estratégico em evidência: os 6 melhores ficam misturados com protótipos e cópias. |
| **Fluxo Royale espalhado** | O projeto principal está espalhado em pelo menos 14 repositórios de gerações diferentes (`Fluxo`, `Fluxo-2.0-*`, `Fluxo-Royale-*`, `*2.1`, `Homolog-*`, `Fluxo5.0-*`, `newFluxo`, `system_royale`, `fluxo-royale-gest-o-inteligente`). Para quem visita, não fica claro qual é o atual. |
| **Cópias de trabalho** | 11 repositórios privados com nomes como `fim`, `att`, `CORRECAO`, `ultimo_ajuste`, `11-12`. Alguns são duplicados: `atualiti` e `full_att` têm o mesmo tamanho (2.706 KB), assim como `ultimo_ajuste` e `CORRECAO` (636 KB). |
| **Vazios** | 3 repositórios sem nenhum arquivo: `Fluxo` e `GringoPizzaria-Back` (públicos) e `novo_ajuste` (privado). |
| **READMEs** | Vários públicos ainda têm o README padrão do Lovable ("Welcome to your Lovable project"), um README de uma linha ou nenhum README. |
| **Nomes** | Quatro estilos misturados: `PascalCase` (ClipPro), `kebab-case` (otica-rinopolis), `snake_case` (SummerDrinks_Cliente) e `MAIÚSCULAS` (CORRECAO, IMAGEM). |
| **Segurança** | Nenhum segredo real encontrado no código atual dos 34 repositórios públicos lidos (os achados eram exemplos em `.env.example`). Único ponto: `swiftflow-hub` versiona um `.env`, mas ele contém só a chave pública do Supabase. A varredura cobriu a versão atual dos arquivos, não o histórico de commits. |

## Resultado esperado depois do plano

| | Antes | Depois |
|---|---|---|
| Repositórios públicos | 37 | 28 (17 ativos + 11 protótipos arquivados) |
| Com descrição | 2 | 39 |
| Com tópicos | 1 | 28 |
| Vazios | 3 | 0 |
| Versões antigas do Fluxo visíveis | 7 | 0 (privadas e arquivadas) |
| README de perfil | não | sim |

Arquivar **não apaga nada**: o repositório fica somente leitura, com o selo
"Archived", e pode ser desarquivado em *Settings → Danger Zone*. Sites já
publicados na Vercel continuam no ar.

## Plano por repositório

### ⭐ Destaques — fixar no perfil (6)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| [Olwe-Studio](https://github.com/Corrar/Olwe-Studio) | público | 2026-10-15 | descrição, tópicos, renomear (opcional) → `olwe-studio` | Fixar no perfil. |
| [ClipPro](https://github.com/Corrar/ClipPro) | público | 2026-10-15 | descrição, tópicos, renomear (opcional) → `clippro` | Fixar no perfil. Já tem um README excelente. |
| [Fluxo-Royale-Frontend](https://github.com/Corrar/Fluxo-Royale-Frontend) | público | 2026-08-11 | descrição, tópicos, renomear (opcional) → `fluxo-royale-frontend` | Fixar no perfil. O README atual tem 1 linha: use o rascunho em modelos/readmes/fluxo-royale-frontend.md. |
| [otica-rinopolis](https://github.com/Corrar/otica-rinopolis) | público | 2026-10-15 | descrição, tópicos | Fixar no perfil. |
| [GringoPizzaria-Front](https://github.com/Corrar/GringoPizzaria-Front) | público | 2026-07-31 | descrição, tópicos, renomear (opcional) → `gringo-pizzaria-frontend` | Fixar no perfil. Se o site estiver publicado, preencha "site" com a URL. |
| [COL-Front](https://github.com/Corrar/COL-Front) | público | 2026-05-15 | — | Fixar no perfil. Já está completo (descrição, tópicos, site e README). O app se chama CLO e o repo COL: vale padronizar. |

### ✅ Ativos públicos — manter e completar (11)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| [Fluxo-Royale-Backend](https://github.com/Corrar/Fluxo-Royale-Backend) | público | 2026-08-11 | descrição, tópicos, renomear (opcional) → `fluxo-royale-backend` |  |
| [SummerDrinks_Cliente](https://github.com/Corrar/SummerDrinks_Cliente) | público | 2026-07-22 | descrição, tópicos, renomear (opcional) → `summer-drinks-cliente` | O README aponta para Corrar/SummerDrinks_Atendimento; o GitHub redireciona o link se renomear. |
| [SummerDrinks_Atendimento](https://github.com/Corrar/SummerDrinks_Atendimento) | público | 2026-07-22 | descrição, tópicos, renomear (opcional) → `summer-drinks-atendimento` | Não tem README.md na raiz: crie um com modelos/README-projeto.md. |
| [DashProject-Frontend](https://github.com/Corrar/DashProject-Frontend) | público | 2026-06-29 | descrição, tópicos, renomear (opcional) → `dash-frontend` | Sem README.md. |
| [DashProject-Backend](https://github.com/Corrar/DashProject-Backend) | público | 2026-06-28 | descrição, tópicos, renomear (opcional) → `dash-backend` |  |
| [Automacao-semana-do-bolo](https://github.com/Corrar/Automacao-semana-do-bolo) | público | 2026-09-18 | descrição, tópicos, renomear (opcional) → `automacao-semana-do-bolo` |  |
| [garcas-burguer](https://github.com/Corrar/garcas-burguer) | público | 2026-04-13 | descrição, tópicos | README ainda é o padrão do Lovable ("TODO"). Há um vídeo .mp4 versionado na raiz: prefira hospedar fora do repo. |
| [Hub-Academico](https://github.com/Corrar/Hub-Academico) | público | 2026-09-10 | descrição, tópicos, renomear (opcional) → `hub-academico` | Sem README.md na raiz (o conteúdo está em PRODUCT.md). |
| [TracoHumano](https://github.com/Corrar/TracoHumano) | público | 2026-10-13 | descrição, tópicos, renomear (opcional) → `traco-humano` | Se for material interno do canal, considere torná-lo privado. |
| [IMAGEM](https://github.com/Corrar/IMAGEM) | público | 2025-05-21 | descrição, tópicos | Não torne privado nem renomeie sem checar: sites podem usar links diretos (raw) dessas imagens. |
| [Ajust-github](https://github.com/Corrar/Ajust-github) | público | 2026-10-15 | descrição, tópicos | Este repositório. |

### 🔒 Ativos privados — manter (8)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| Fluxo5.0-Backend | privado | 2026-10-15 | descrição | Versão atual do Fluxo (privada). |
| Fluxo5.0-Front | privado | 2026-10-15 | descrição | Versão atual do Fluxo (privada). |
| Motor-de-busca-de-filmes | privado | 2026-10-15 | descrição | Privado, mas com site publicado (cinebusca): se quiser mostrar no portfólio, torne público. |
| Emissao-de-notas-API | privado | 2026-06-30 | descrição |  |
| Royale-Vision | privado | 2026-10-15 | — | Privado e sem acesso de leitura nesta auditoria: escreva a descrição você mesmo. |
| Radar-Local | privado | 2026-09-18 | — | Privado e sem acesso de leitura nesta auditoria: escreva a descrição você mesmo. |
| fatec-central-hub | privado | 2026-08-26 | — | Parece ligado ao Hub-Academico; se for só um protótipo dele, arquive. |
| lume-casa-charmosa | privado | 2026-08-14 | — | Privado e sem acesso de leitura nesta auditoria: escreva a descrição você mesmo. |

### 🧪 Protótipos — arquivar (17)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| [savory-sweet-slices](https://github.com/Corrar/savory-sweet-slices) | público | 2026-06-20 | descrição, tópicos, arquivar | Substituído por GringoPizzaria-Front. |
| [projeto-garca](https://github.com/Corrar/projeto-garca) | público | 2026-06-14 | descrição, tópicos, arquivar | Material de design já implementado em garcas-burguer. |
| [dev-companion](https://github.com/Corrar/dev-companion) | público | 2026-05-13 | descrição, tópicos, arquivar |  |
| [happy-stock-in](https://github.com/Corrar/happy-stock-in) | público | 2026-05-13 | descrição, tópicos, arquivar |  |
| [3d-forge-hub](https://github.com/Corrar/3d-forge-hub) | público | 2026-05-08 | descrição, tópicos, arquivar | A ideia virou o módulo Produção 3D do Fluxo Royale. |
| [procurement-navigator](https://github.com/Corrar/procurement-navigator) | público | 2026-05-06 | descrição, tópicos, arquivar |  |
| [client-task-hub](https://github.com/Corrar/client-task-hub) | público | 2026-04-25 | descrição, tópicos, arquivar |  |
| [swiftflow-hub](https://github.com/Corrar/swiftflow-hub) | público | 2026-04-23 | descrição, tópicos, arquivar | Tem um .env versionado (só a chave pública do Supabase, que é feita para o navegador). Confirme que o RLS está ativo nas tabelas. |
| [trello-clone-detailed](https://github.com/Corrar/trello-clone-detailed) | público | 2026-03-04 | descrição, tópicos, arquivar |  |
| [operalytics-hub](https://github.com/Corrar/operalytics-hub) | público | 2026-02-19 | descrição, tópicos, arquivar |  |
| [visual-card-studio](https://github.com/Corrar/visual-card-studio) | público | 2026-02-05 | descrição, tópicos, arquivar |  |
| burger-buddy-system | privado | 2026-03-27 | arquivar | Privado; criado no mesmo dia que garcas-burguer (provável origem dele). |
| stock-harmony | privado | 2026-01-27 | arquivar | Privado, sem atividade desde jan/2026. |
| stock-flow | privado | 2025-11-21 | arquivar | Privado, sem atividade desde nov/2025. |
| pdf-stock-sync | privado | 2025-11-10 | arquivar | Privado, sem atividade desde nov/2025. |
| nfe-autofill | privado | 2025-10-11 | arquivar | Privado, sem atividade desde out/2025. |
| gestao-pronta | privado | 2025-09-19 | arquivar | Privado, sem atividade desde set/2025. |

### 🗄️ Versões antigas do Fluxo — privar e arquivar (7)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| [Fluxo-2.0-Frontend](https://github.com/Corrar/Fluxo-2.0-Frontend) | público | 2025-12-18 | descrição, privar, arquivar | O site já publicado continua no ar depois de privar/arquivar. |
| [Fluxo-2.0-Backend](https://github.com/Corrar/Fluxo-2.0-Backend) | público | 2025-12-19 | descrição, privar, arquivar |  |
| [Fluxo-Royale-Frontend2.1](https://github.com/Corrar/Fluxo-Royale-Frontend2.1) | público | 2026-03-25 | descrição, privar, arquivar |  |
| [Fluxo-Royale-Backend2.1](https://github.com/Corrar/Fluxo-Royale-Backend2.1) | público | 2026-03-16 | descrição, privar, arquivar |  |
| [Homolog-FluxoFront](https://github.com/Corrar/Homolog-FluxoFront) | público | 2026-06-15 | descrição, privar, arquivar | Confirme que não usa mais a homologação antes de arquivar (o Fluxo atual é o 5.0). |
| [Homolog-FluxoBack](https://github.com/Corrar/Homolog-FluxoBack) | público | 2026-06-15 | descrição, privar, arquivar | Confirme que não usa mais a homologação antes de arquivar (o Fluxo atual é o 5.0). |
| [fluxo-royale-gest-o-inteligente](https://github.com/Corrar/fluxo-royale-gest-o-inteligente) | público | 2026-02-12 | descrição, privar, arquivar |  |

### 🧹 Cópias de trabalho (privadas) — arquivar (11)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| 11-12 | privado | 2025-12-11 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| att | privado | 2025-12-16 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| atualiti | privado | 2025-12-18 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| full_att | privado | 2026-01-05 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| corrigir-final | privado | 2025-12-10 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| fim | privado | 2025-12-09 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| Ajudes_entrada | privado | 2025-12-09 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| ultimo_ajuste | privado | 2025-12-08 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| CORRECAO | privado | 2025-12-08 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| newFluxo | privado | 2025-12-17 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |
| system_royale | privado | 2025-12-05 | arquivar | Candidato a exclusão depois de conferir que nada falta no Fluxo atual. |

### 🗑️ Vazios — excluir (3)

| Repositório | Visib. | Última atividade | Ação | Observação |
|---|---|---|---|---|
| [Fluxo](https://github.com/Corrar/Fluxo) | público | 2025-12-04 | **excluir** | Público e vazio (0 KB). |
| [GringoPizzaria-Back](https://github.com/Corrar/GringoPizzaria-Back) | público | 2026-07-26 | **excluir** | Público e vazio (0 KB). |
| novo_ajuste | privado | 2025-12-11 | **excluir** | Privado e vazio (0 KB). |

