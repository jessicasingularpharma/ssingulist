# app/routers/ordem_compra_detalhes.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.ordem_compra import (FranquiaOrdemCreate, FranquiaOrdemOut,
                                     OrdemCompraDetalhesCreate,
                                     OrdemCompraDetalhesOut,
                                     PendenciaSubstanciaCreate,
                                     PendenciaSubstanciaOut)
from app.models.usuario import Usuario
from app.services import ordem_compra_service

router = APIRouter(prefix="/ordem-compra/gerenciar", tags=["Admin - Gerenciar Ordens"])


# --- DETALHES ---
@router.post("/detalhes", response_model=OrdemCompraDetalhesOut)
def criar_detalhes_ordem(
    detalhes_data: OrdemCompraDetalhesCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return ordem_compra_service.criar_detalhes_ordem(db, detalhes_data)


# --- PENDÊNCIAS ---
@router.post("/pendencias", response_model=PendenciaSubstanciaOut)
def adicionar_pendencia(
    pendencia_data: PendenciaSubstanciaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return ordem_compra_service.adicionar_pendencia_substancia(db, pendencia_data)


# --- FRANQUIAS ---
@router.post("/franquias", response_model=FranquiaOrdemOut)
def adicionar_franquia(
    franquia_data: FranquiaOrdemCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return ordem_compra_service.adicionar_franquia_ordem(db, franquia_data)
