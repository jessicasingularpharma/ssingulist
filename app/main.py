# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import minhas_solicitacoes

# Carrega variáveis de ambiente
load_dotenv()

# Cria o app
app = FastAPI(title="Supply Control API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa todos os routers
from app.routers import (
    auth,
    solicitacao,
    usuario,
    produto_router,
    ordem_compra,
    ordem_compra_detalhes,
    minhas_solicitacoes,
    debug_ordens,
)

# Registra os routers
app.include_router(auth.router)
app.include_router(solicitacao.router)
app.include_router(usuario.router)
app.include_router(produto_router.router)
app.include_router(ordem_compra.router)
app.include_router(ordem_compra_detalhes.router)
app.include_router(minhas_solicitacoes.router)
app.include_router(debug_ordens.router)

# Rota raiz para teste
@app.get("/")
def root():
    return {"message": "🚀 API do Sistema de Suprimentos está online!"}
