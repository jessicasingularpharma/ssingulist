﻿
# Sistema de Controle de Suprimentos

Este projeto é um sistema completo para controle de suprimentos, construído com uma arquitetura moderna e escalável. Ele contempla automação de solicitações, gestão de estoque, integração com ERP e alertas por e-mail.

---

## Visão Geral da Stack

| Camada         | Tecnologia                                       | Função                                                                 |
|----------------|--------------------------------------------------|------------------------------------------------------------------------|
| **Frontend**   | ReactJS, Bootstrap                              | Interface de usuário responsiva e moderna                             |
| **Backend**    | FastAPI, SQLAlchemy, Pydantic                    | API REST, lógica de negócios e validação                              |
| **Banco**      | PostgreSQL                                       | Armazenamento relacional e persistente de dados                       |
| **Autenticação** | OAuth2 + JWT                                   | Segurança com controle de acesso e tokens                             |
| **Automação**  | Celery, Redis, SMTP                              | Tarefas assíncronas (e-mail, sincronização, alertas)                  |
| **Integração** | pandas, pyodbc, firebirdsql                      | Conexão e extração de dados do ERP legado (Firebird/ODBC)             |
| **Infraestrutura** | Docker, NGINX, Gunicorn, GitHub Actions    | Contêineres, deploy, proxy, e CI/CD automatizado                      |
| **Extras**     | Grafana, logs de atividade                       | Monitoramento e auditoria                                             |

---

## Sumário

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação do Projeto](#instalação-do-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Ambiente Backend com Poetry](#ambiente-backend-com-poetry)
- [Executando o Backend](#executando-o-backend)
- [Testes com Pytest](#testes-com-pytest)
- [Qualidade de Código com Pre-commit](#qualidade-de-código-com-pre-commit)
- [Documentação da API](#documentação-da-api)
- [Instruções para Colaboradores](#instruções-para-colaboradores)
- [Comandos Úteis](#comandos-úteis)
- [Próximos Passos](#próximos-passos)

---

## Tecnologias Utilizadas

(veja a tabela da Visão Geral da Stack)

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Node.js (para o frontend React)
- Git instalado
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) instalado:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

---

## Instalação do Projeto

### 1. Clone o projeto

```bash
git clone https://github.com/jessicasingularpharma/ssingulist.git
cd supply_control_system
```

### 2. Execute o script de estrutura inicial

Use **Git Bash** ou **WSL** (não PowerShell):

```bash
bash setup.sh
```

Esse script criará toda a estrutura de diretórios e arquivos iniciais.

---

## Estrutura do Projeto

```
supply_control_system/
├── frontend/               # Interface do usuário com React
├── backend/                # API com FastAPI
│   ├── app/                # Código principal do backend
│   ├── main.py             # Ponto de entrada FastAPI
│   ├── celery_worker.py    # Worker para tarefas assíncronas
│   ├── tests/              # Testes automatizados com pytest
│   ├── .env.example        # Exemplo de variáveis de ambiente
├── .vscode/                # Configurações do VS Code
├── docker-compose.yml      # Orquestração dos containers
├── README.md
└── .github/workflows/      # CI/CD com GitHub Actions
```

---

## Ambiente Backend com Poetry

### 1. Navegue até o backend

```bash
cd backend
```

### 2. Instale as dependências

```bash
poetry install
```

> Se aparecer erro de `No file/folder found for package`, adicione ao `pyproject.toml`:
```toml
packages = [{ include = "app" }]
```

### 3. Ative o ambiente virtual

```bash
poetry shell
```

---

## Executando o Backend

Dentro do ambiente do Poetry:

```bash
uvicorn main:app --reload
```

### Acessos:

- API: http://127.0.0.1:8000
- Docs Swagger: http://127.0.0.1:8000/docs
- Docs Redoc: http://127.0.0.1:8000/redoc

---

## Testes com Pytest

```bash
pytest
```

O projeto possui uma estrutura `/backend/tests` com testes automatizados utilizando FastAPI TestClient.

---

## Qualidade de Código com Pre-commit

1. Instale os pacotes:

```bash
poetry add --group dev pre-commit black flake8 isort mypy
```

2. Instale os hooks:

```bash
pre-commit install
```

3. Rode manualmente se quiser:

```bash
pre-commit run --all-files
```

Os hooks incluem: `black`, `flake8`, `isort`, `mypy`, `trailing-whitespace`, `end-of-file-fixer`.

---

## Documentação da API

A FastAPI gera a documentação automática acessível via `/docs`.

Aqui estarão listados todos os endpoints da API RESTful com parâmetros, exemplos de resposta e testes integrados.

---

## Instruções para Colaboradores

1. Clone o repositório:

```bash
git clone <repo-url>
cd supply_control_system
```

2. Configure o backend:

```bash
cd backend
poetry install
poetry shell
```

3. Inicie o servidor local:

```bash
uvicorn main:app --reload
```

4. Acesse no navegador:

- http://127.0.0.1:8000 → resposta padrão
- http://127.0.0.1:8000/docs → documentação Swagger

---

## Comandos Úteis

### Rodar servidor de desenvolvimento

```bash
uvicorn main:app --reload
```

### Rodar worker Celery

```bash
celery -A app.tasks worker --loglevel=info
```

### Exportar dependências para `requirements.txt` (opcional)

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

## Próximos Passos

- Criar modelos SQLAlchemy (`models/`)
- Criar schemas Pydantic (`schemas/`)
- Criar rotas (`routers/`)
- Criar lógica de negócio (`services/`)
- Criar tarefas automáticas (`tasks/`)
- Configurar NGINX e Docker
- Conectar com banco PostgreSQL
- Criar login com OAuth2
- Configurar Grafana
- Implementar integração com ERP via `pyodbc` e `firebirdsql`

---

Este projeto é mantido e desenvolvido com foco em automação e confiabilidade nos processos de suprimentos.
