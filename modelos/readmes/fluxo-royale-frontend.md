<!--
  Rascunho de README para Corrar/Fluxo-Royale-Frontend (o atual tem 1 linha).
  Montado a partir das rotas e dependências do próprio código.
  Revise, adicione prints das telas e cole como README.md na raiz do repo.
-->

<div align="center">

<img src="public/logo-royale.png" alt="Fluxo Royale" width="96" />

# Fluxo Royale

Sistema de controle de estoque, compras e requisições por setor.

[![Demo](https://img.shields.io/badge/demo-fluxo--royale.vercel.app-22c55e?style=flat-square&logo=vercel)](https://fluxo-royale.vercel.app)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-0F172A?style=flat-square&logo=tailwindcss&logoColor=38BDF8)

<!-- ![Painel](docs/painel.png) -->

</div>

## ✨ Funcionalidades

| Área | O que tem |
|---|---|
| **Estoque** | Visão geral, entradas, saídas, movimentações, estoque baixo, cálculo de estoque mínimo e produtos arquivados |
| **Requisições** | Pedidos dos setores, "minhas requisições", separações, reposições e devoluções por setor |
| **Produção 3D** | Painel, catálogo, demandas e fila de produção de peças impressas em 3D |
| **Gestão** | Clientes, conciliação de viagens, importação de XML, relatórios com gráficos e exportação em PDF/Excel |
| **Equipe** | Quadros de tarefas (inclusive da elétrica), lembretes, calculadora e busca global |
| **Administração** | Usuários, permissões por tela, auditoria de ações e configurações do sistema |
| **App** | Instalável (PWA) com notificações push |

## 🛠️ Tecnologias

- **React 18 + TypeScript** com **Vite**
- **Tailwind CSS** + **shadcn/ui** (Radix) e animações com **GSAP** / **Framer Motion**
- **TanStack Query**, **React Hook Form** + **Zod**
- **Recharts** (gráficos), **jsPDF** e **SheetJS** (exportação), **dnd-kit** (arrastar e soltar)
- **Socket.IO** para atualizações em tempo real
- API própria: [Fluxo-Royale-Backend](https://github.com/Corrar/Fluxo-Royale-Backend) (Node.js, Express, PostgreSQL)

## 🚀 Como rodar

```bash
git clone https://github.com/Corrar/Fluxo-Royale-Frontend.git
cd Fluxo-Royale-Frontend
npm install
echo "VITE_API_URL=http://localhost:3000" > .env   # endereço da API
npm run dev
```

| Script | O que faz |
|---|---|
| `npm run dev` | servidor de desenvolvimento |
| `npm run build` | checagem de tipos + build de produção |
| `npm run lint` | ESLint |
| `npm run preview` | serve o build localmente |

## 📄 Licença

Todos os direitos reservados.
