from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.solicitacao_laboratorio import (
    SolicitacaoLaboratorio,
    SolicitacaoLaboratorioStatusHistorico,
    SolicitacaoLaboratorioItem
)
from app.models.usuario import Usuario
from app.schemas.solicitacao_laboratorio import SolicitacaoLaboratorioStatusUpdate


def criar_solicitacao_laboratorio(db: Session, solicitacao: SolicitacaoLaboratorio) -> SolicitacaoLaboratorio:
    solicitacao.status = "aberto"
    db.add(solicitacao)
    db.commit()
    db.refresh(solicitacao)
    registrar_historico_status_laboratorio(db, solicitacao.id, solicitacao.status, solicitacao.solicitante_id)
    return solicitacao


def atualizar_status_solicitacao_com_historico(
    db: Session,
    solicitacao_id: int,
    novo_status: SolicitacaoLaboratorioStatusUpdate,
    usuario: Usuario
) -> SolicitacaoLaboratorio:
    solicitacao = db.query(SolicitacaoLaboratorio).filter(SolicitacaoLaboratorio.id == solicitacao_id).first()

    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação de laboratório não encontrada")

    if solicitacao.status == novo_status.status:
        return solicitacao  # Nada muda se o status for o mesmo

    solicitacao.status = novo_status.status
    db.commit()
    db.refresh(solicitacao)

    registrar_historico_status_laboratorio(db, solicitacao.id, novo_status.status, usuario.id)
    return solicitacao


def registrar_historico_status_laboratorio(db: Session, solicitacao_id: int, status: str, alterado_por: int):
    historico = SolicitacaoLaboratorioStatusHistorico(
        solicitacao_id=solicitacao_id,
        status=status,
        alterado_por=alterado_por
    )
    db.add(historico)
    db.commit()
    return historico