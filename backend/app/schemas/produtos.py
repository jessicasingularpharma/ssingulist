# backend/app/schemas/produto.py
from pydantic import BaseModel


class ProdutoSugestaoOut(BaseModel):
    codigo: int
    descricao: str
    unidade: str
