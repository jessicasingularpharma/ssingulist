from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Controle de Suprimentos",
    description="API para gerenciamento de solicitações, estoques e integração com ERP",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "🚀 Backend da API de suprimentos está rodando!"}
