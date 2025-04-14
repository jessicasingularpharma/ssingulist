from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.ordem_compra import (OrdemCompra, OrdemCompraDetalhes,
                                     OrdemCompraItem)
from app.models.usuario import Usuario
from app.schemas.ordem_compra import (OrdemCompraCreate,
                                      OrdemCompraDetalhesUpdate,
                                      OrdemCompraOut, OrdemCompraStatusUpdate)
from app.services.ordem_compra_service import criar_ordem_compra

router = APIRouter(prefix="/ordem-compra", tags=["Ordem de Compra"])


@router.get("/listar-todas", response_model=List[OrdemCompraOut])
def listar_ordens_completas(db: Session = Depends(get_db)):
    ordens = db.query(OrdemCompra).all()
    for ordem in ordens:
        ordem.tipo = (
            "suprimentos"  # pode ser substituído por campo real se adicionado no banco
        )
    return ordens


@router.post(
    "/criar", response_model=OrdemCompraOut, status_code=status.HTTP_201_CREATED
)
def criar_ordem(
    dados: OrdemCompraCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    if dados.solicitante_id != usuario.id:
        raise HTTPException(status_code=403, detail="Solicitante inválido.")

    nova_ordem = OrdemCompra(
        solicitante_id=dados.solicitante_id,
        tipo="suprimentos",  # ✅ tipo definido como suprimentos
    )

    nova_ordem = criar_ordem_compra(db, nova_ordem)

    for item in dados.itens:
        novo_item = OrdemCompraItem(
            ordem_id=nova_ordem.id,
            codigo_produto=item.codigo_produto,
            nome_produto=item.nome_produto,
            quantidade=item.quantidade,
            unidade=item.unidade,
            observacao=item.observacao,
            data_necessidade=item.data_necessidade,
            urgente=item.urgente,
        )
        db.add(novo_item)

    db.commit()
    db.refresh(nova_ordem)
    return nova_ordem


@router.put("/atualizar-detalhes/{ordem_id}", response_model=OrdemCompraOut)
def atualizar_detalhes_ordem(
    ordem_id: int,
    detalhes: OrdemCompraDetalhesUpdate,
    db: Session = Depends(get_db),
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


@router.put("/atualizar-status/{ordem_id}")
def atualizar_status_ordem(
    ordem_id: int,
    status_data: OrdemCompraStatusUpdate,
    db: Session = Depends(get_db),
):
    ordem = db.query(OrdemCompra).filter(OrdemCompra.id == ordem_id).first()
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")

    ordem.status = status_data.status
    db.commit()
    return {"mensagem": "Status atualizado com sucesso"}


@router.delete("/deletar/{ordem_id}", status_code=204)
def deletar_ordem(
    ordem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ordem = (
        db.query(OrdemCompra)
        .filter(
            OrdemCompra.id == ordem_id,
            OrdemCompra.solicitante_id == usuario.id,
        )
        .first()
    )
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    db.delete(ordem)
    db.commit()
    return
