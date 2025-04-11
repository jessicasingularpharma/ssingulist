# backend/app/routers/produto_router.py
from fastapi import APIRouter, Depends, Query
from typing import List
from app.services.produto_service import buscar_produtos_por_nome
from app.auth.auth_bearer import get_current_user
from app.models.usuario import Usuario
from app.schemas.produtos import ProdutoSugestaoOut

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/buscar", response_model=List[ProdutoSugestaoOut])
def buscar_produtos(
    nome: str = Query(..., min_length=2),
    usuario: Usuario = Depends(get_current_user)
):
    produtos = buscar_produtos_por_nome(nome)
    return produtos
