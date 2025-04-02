from fastapi import FastAPI
from app.routers import solicitacao

app = FastAPI()

app.include_router(solicitacao.router)

@app.get("/")
def root():
    return {"message": "API online!"}
