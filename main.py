from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import test_minhas  # <- ao invés de minhas_solicitacoes
from app.routers import produto_router

# Carrega variáveis
load_dotenv()

app = FastAPI(title="Supply Control API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Agora sim importa os routers DEPOIS do app estar pronto
from app.routers import (
    auth,
    solicitacao,
    usuario,
    produto_router,
    ordem_compra,
    ordem_compra_detalhes,
    #minhas_solicitacoes,
)

# ✅ E inclui os routers
app.include_router(auth.router)
app.include_router(solicitacao.router)
app.include_router(usuario.router)
app.include_router(produto_router.router)
app.include_router(ordem_compra.router)
app.include_router(ordem_compra_detalhes.router)
#app.include_router(minhas_solicitacoes.router)
app.include_router(test_minhas.router)
app.include_router(produto_router.router)

@app.get("/")
def root():
    return {"message": "🚀 API do Sistema de Suprimentos está online!"}
