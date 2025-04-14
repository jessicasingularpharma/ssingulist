from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.ordem_compra import (OrdemCompra, OrdemCompraDetalhes,
                                     OrdemCompraStatusHistorico)
from app.models.usuario import Usuario
from app.schemas.ordem_compra import (OrdemCompraDetalhesUpdate,
                                      OrdemCompraOut,
                                      OrdemCompraStatusHistoricoOut,
                                      OrdemCompraStatusUpdate)
from app.services import ordem_compra_service  # ✅

router = APIRouter(prefix="/ordem-compra", tags=["Ordem de Compra"])


@router.get("/listar-todas", response_model=List[OrdemCompraOut])
def listar_ordens_completas(db: Session = Depends(get_db)):
    ordens = db.query(OrdemCompra).all()
    for ordem in ordens:
        ordem.tipo = "suprimentos"
    return ordens


@router.put("/atualizar-detalhes/{ordem_id}", response_model=OrdemCompraOut)
def atualizar_detalhes_ordem(
    ordem_id: int, detalhes: OrdemCompraDetalhesUpdate, db: Session = Depends(get_db)
):
    ordem = db.query(OrdemCompra).filter(OrdemCompra.id == ordem_id).first()
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")

    if not ordem.detalhes:
        ordem.detalhes = OrdemCompraDetalhes(ordem_id=ordem_id)
        db.add(ordem.detalhes)

    for field, value in detalhes.dict(exclude_unset=True).items():
        setattr(ordem.detalhes, field, value)

    db.commit()
    db.refresh(ordem)
    return ordem


@router.put("/atualizar-status/{ordem_id}", response_model=OrdemCompraOut)
def atualizar_status_ordem(
    ordem_id: int,
    status_data: OrdemCompraStatusUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ordem = ordem_compra_service.atualizar_status_ordem_com_historico(
        db=db, ordem_id=ordem_id, novo_status=status_data.status, usuario_id=usuario.id
    )

    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")

    return ordem


@router.delete("/deletar/{ordem_id}", status_code=204)
def deletar_ordem(
    ordem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ordem = (
        db.query(OrdemCompra)
        .filter(OrdemCompra.id == ordem_id, OrdemCompra.solicitante_id == usuario.id)
        .first()
    )
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    db.delete(ordem)
    db.commit()
    return


@router.get("/{ordem_id}/historico", response_model=List[OrdemCompraStatusHistoricoOut])
def listar_historico_status(
    ordem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    historico = (
        db.query(OrdemCompraStatusHistorico)
        .filter(OrdemCompraStatusHistorico.ordem_id == ordem_id)
        .order_by(OrdemCompraStatusHistorico.data_alteracao.desc())
        .all()
    )
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico não encontrado.")
    return historico
