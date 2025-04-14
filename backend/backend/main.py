from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import auth  # ⬅️ Importa as rotas de autenticação
from app.routers import solicitacao

load_dotenv()

app = FastAPI()

# Inclui as rotas
app.include_router(solicitacao.router)
app.include_router(auth.router)  # ⬅️ Registra as rotas de login e /usuarios/me


@app.get("/")
def root():
    return {"message": "API online!"}
