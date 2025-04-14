from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import auth, solicitacao, usuario

load_dotenv()

app = FastAPI()

app.include_router(solicitacao.router)
app.include_router(auth.router)
app.include_router(usuario.router)  # ➕ Adicionada aqui


@app.get("/")
def root():
    return {"message": "API online!"}
