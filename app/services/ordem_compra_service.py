# app/services/ordem_compra_service.py
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ordem_compra import (FranquiaOrdem, FranquiaOrdemCreate,
                                     OrdemCompra, OrdemCompraDetalhes,
                                     OrdemCompraDetalhesCreate,
                                     OrdemCompraStatusHistorico,
                                     PendenciaSubstancia,
                                     PendenciaSubstanciaCreate,
                                     StatusOrdemCompra)
from app.models.usuario import Usuario
from app.schemas.ordem_compra import OrdemCompraStatusUpdate


# --- Atualização de Status com Histórico ---
def atualizar_status_ordem_com_historico(
    db: Session, ordem_id: int, novo_status: OrdemCompraStatusUpdate, usuario: Usuario
):
    if not usuario.is_admin:
        raise HTTPException(
            status_code=403, detail="Apenas administradores podem alterar o status"
        )

    ordem = db.query(OrdemCompra).filter(OrdemCompra.id == ordem_id).first()
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem de compra não encontrada")

    ordem.status = novo_status.status
    db.commit()
    db.refresh(ordem)

    registrar_status_historico(db, ordem.id, novo_status.status, usuario.id)
    return ordem


# --- Registro de Histórico ---
def registrar_status_historico(
    db: Session, ordem_id: int, novo_status: StatusOrdemCompra, usuario_id: int
):
    historico = OrdemCompraStatusHistorico(
        ordem_id=ordem_id, status=novo_status, alterado_por=usuario_id
    )
    db.add(historico)
    db.commit()
    return historico


# --- Criação de Ordem com Identificador e Histórico ---
def gerar_identificador_ordem(db: Session) -> str:
    ultimo = db.query(func.max(OrdemCompra.id)).scalar() or 0
    return f"ORD-{ultimo + 1:04d}"


def criar_ordem_compra(db: Session, ordem: OrdemCompra) -> OrdemCompra:
    ordem.status = StatusOrdemCompra.aberto  # força o status inicial
    ordem.identificador = gerar_identificador_ordem(db)
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    registrar_status_historico(db, ordem.id, ordem.status, ordem.solicitante_id)
    return ordem


# --- Detalhes da Ordem de Compra ---
def criar_detalhes_ordem(
    db: Session, detalhes_data: OrdemCompraDetalhesCreate
) -> OrdemCompraDetalhes:
    detalhes = OrdemCompraDetalhes(**detalhes_data.dict())
    db.add(detalhes)
    db.commit()
    db.refresh(detalhes)
    return detalhes


def atualizar_detalhes_ordem(
    db: Session, ordem_id: int, novos_dados: dict
) -> OrdemCompraDetalhes:
    detalhes = db.query(OrdemCompraDetalhes).filter_by(ordem_id=ordem_id).first()
    if detalhes:
        for campo, valor in novos_dados.items():
            setattr(detalhes, campo, valor)
        db.commit()
        db.refresh(detalhes)
    return detalhes


# --- Pendências de Substâncias ---
def adicionar_pendencia_substancia(
    db: Session, pendencia_data: PendenciaSubstanciaCreate
) -> PendenciaSubstancia:
    pendencia = PendenciaSubstancia(**pendencia_data.dict())
    db.add(pendencia)
    db.commit()
    db.refresh(pendencia)
    return pendencia


def listar_pendencias_por_ordem(db: Session, ordem_id: int):
    return db.query(PendenciaSubstancia).filter_by(ordem_id=ordem_id).all()


# --- Franquias ---
def adicionar_franquia_ordem(
    db: Session, franquia_data: FranquiaOrdemCreate
) -> FranquiaOrdem:
    franquia = FranquiaOrdem(**franquia_data.dict())
    db.add(franquia)
    db.commit()
    db.refresh(franquia)
    return franquia


def listar_franquias_por_ordem(db: Session, ordem_id: int):
    return db.query(FranquiaOrdem).filter_by(ordem_id=ordem_id).all()


# --- Listagem por Usuário ---
def listar_ordens_por_usuario(db: Session, usuario_id: int) -> List[OrdemCompra]:
    return (
        db.query(OrdemCompra)
        .filter(OrdemCompra.solicitante_id == usuario_id)
        .order_by(OrdemCompra.criado_em.desc())
        .all()
    )
