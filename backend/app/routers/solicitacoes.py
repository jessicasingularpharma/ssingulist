# app/routers/solicitacoes.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.solicitacao_laboratorio import (SolicitacaoLaboratorio,
                                                SolicitacaoLaboratorioItem,
                                                SolicitacaoStatusHistorico)
from app.models.usuario import Usuario
from app.schemas.solicitacao_laboratorio import (SolicitacaoLaboratorioCreate,
                                                 SolicitacaoLaboratorioOut)

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações"])


@router.post("/", response_model=SolicitacaoLaboratorioOut)
def criar_solicitacao(
    dados: SolicitacaoLaboratorioCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    nova_solicitacao = SolicitacaoLaboratorio(
        solicitante_id=usuario.id, status="aberto", criado_em=datetime.utcnow()
    )
    db.add(nova_solicitacao)
    db.commit()
    db.refresh(nova_solicitacao)

    # Adiciona os itens
    for item in dados.itens:
        item_db = SolicitacaoLaboratorioItem(
            solicitacao_id=nova_solicitacao.id, **item.dict()
        )
        db.add(item_db)

    # Adiciona histórico inicial
    historico = SolicitacaoStatusHistorico(
        solicitacao_id=nova_solicitacao.id, status="aberto", alterado_por=usuario.id
    )
    db.add(historico)

    db.commit()
    db.refresh(nova_solicitacao)
    return nova_solicitacao
