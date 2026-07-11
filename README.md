# 📦 Estoque Inteligente

Sistema de controle de estoque para pequeno varejo que **prevê quando cada produto vai zerar**, com base no histórico de vendas — evitando perda de venda por ruptura de estoque.

## 🎯 O problema

Pequenas lojas e varejistas frequentemente perdem vendas porque não sabem quando um produto vai faltar. O controle manual de estoque não avisa com antecedência, e a reposição só acontece depois que o produto já zerou.

Esse projeto resolve isso calculando, com base no ritmo de vendas de cada produto, **quantos dias faltam até o estoque zerar**, permitindo que o lojista se antecipe.

## ✨ Funcionalidades

- Cadastro, edição e remoção de produtos
- Registro de vendas (com validação de estoque insuficiente)
- Registro de reposição de estoque
- **Previsão automática de ruptura**, baseada na média de vendas dos últimos 30 dias
- Dashboard visual com indicador de risco (verde/amarelo/vermelho)
- Endpoint de alertas para produtos em risco de ruptura
- Testes automatizados no backend

## 🛠️ Stack utilizada

**Backend**
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pytest

**Frontend**
- React
- TypeScript
- Vite
- React Router
- Axios

## 🧠 Como funciona a previsão

O cálculo é feito com base nas vendas registradas nos últimos 30 dias:
média de vendas por dia = total vendido no período / 30
dias até zerar = estoque atual / média de vendas por dia


Com base nesse resultado, o produto recebe um status:

| Status | Condição |
|---|---|
| 🟢 OK | mais de 15 dias até zerar |
| 🟡 Atenção | entre 7 e 15 dias até zerar |
| 🔴 Crítico | 7 dias ou menos até zerar |
| ⚪ Sem dados | nenhuma venda registrada no período |

## 🚀 Como rodar o projeto

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

### Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`.

> **Importante:** o backend precisa estar rodando para o frontend funcionar corretamente.

## 🧪 Rodando os testes

```bash
cd backend
source venv/bin/activate
pytest -v
```

## 📁 Estrutura do projeto

estoque-inteligente/
├── backend/
│   ├── routers/          # Endpoints da API
│   ├── tests/             # Testes automatizados
│   ├── main.py             # Ponto de entrada da aplicação
│   ├── models.py           # Modelos do banco de dados
│   ├── schemas.py          # Validação de dados (Pydantic)
│   ├── forecasting.py      # Lógica de previsão de ruptura
│   └── database.py         # Configuração do banco
│
└── frontend/
└── src/
├── pages/           # Telas da aplicação
├── services/         # Comunicação com a API
└── types/            # Tipos TypeScript

## 🔮 Possíveis melhorias futuras

- Migrar o banco para PostgreSQL em produção
- Adicionar autenticação de usuários
- Previsão com modelos estatísticos mais robustos (ex: considerando sazonalidade)
- Central de alertas dedicada no frontend
- Gráfico de histórico de vendas por produto
- Deploy em produção (backend e frontend)

---

Desenvolvido como projeto de portfólio, simulando um problema real de gestão de estoque em pequenos negócios.
