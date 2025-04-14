# ✅ ROUTER - backend/app/routers/solicitacoes_laboratorio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.solicitacao_laboratorio import (
    SolicitacaoLaboratorio, SolicitacaoLaboratorioItem,
    SolicitacaoLaboratorioStatusHistorico)
from app.models.usuario import Usuario
from app.schemas.solicitacao_laboratorio import SolicitacaoLaboratorioCreate

router = APIRouter(prefix="/solicitacoes", tags=["Solicitacoes de Laboratorio"])


@router.post("/", status_code=201)
def criar_solicitacao(
    solicitacao: SolicitacaoLaboratorioCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    nova = SolicitacaoLaboratorio(
        solicitante_id=solicitacao.solicitante_id, status="aberto"
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)

    for item in solicitacao.itens:
        novo_item = SolicitacaoLaboratorioItem(solicitacao_id=nova.id, **item.dict())
        db.add(novo_item)

    historico = SolicitacaoLaboratorioStatusHistorico(
        solicitacao_id=nova.id, status="aberto", alterado_por=usuario.id
    )
    db.add(historico)
    db.commit()
    return {"mensagem": "Solicitacao criada", "id": nova.id}
