### ✅ app/services/solicitacao_service.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.solicitacao import SolicitacaoLaboratorio, SolicitacaoItem
from app.schemas.solicitacao import SolicitacaoCreate, SolicitacaoUpdate

def criar_solicitacao(
    db: Session, solicitacao_data: SolicitacaoCreate, usuario_id: int
) -> SolicitacaoLaboratorio:
    nova_solicitacao = SolicitacaoLaboratorio(
        solicitante_id=usuario_id,
        status="em_andamento",
        criado_em=datetime.utcnow(),
    )

    db.add(nova_solicitacao)
    db.flush()  # Para obter o ID da solicitação antes de adicionar os itens

    for item_data in solicitacao_data.itens:
        item = SolicitacaoItem(
            solicitacao_id=nova_solicitacao.id,
            codigo_produto=item_data.codigo_produto,
            nome_produto=item_data.nome_produto,
            quantidade=item_data.quantidade,
            unidade=item_data.unidade,
        )
        db.add(item)

    db.commit()
    db.refresh(nova_solicitacao)
    return nova_solicitacao

def listar_solicitacoes_por_usuario(
    db: Session, usuario_id: int
) -> List[SolicitacaoLaboratorio]:
    return (
        db.query(SolicitacaoLaboratorio)
        .filter(SolicitacaoLaboratorio.solicitante_id == usuario_id)
        .order_by(SolicitacaoLaboratorio.criado_em.desc())
        .all()
    )

def buscar_solicitacao_por_id(
    db: Session, solicitacao_id: int, usuario_id: int
) -> Optional[SolicitacaoLaboratorio]:
    return (
        db.query(SolicitacaoLaboratorio)
        .filter(
            SolicitacaoLaboratorio.id == solicitacao_id,
            SolicitacaoLaboratorio.solicitante_id == usuario_id,
        )
        .first()
    )

def atualizar_solicitacao(
    db: Session,
    solicitacao_id: int,
    usuario_id: int,
    solicitacao_data: SolicitacaoUpdate,
) -> Optional[SolicitacaoLaboratorio]:
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id, usuario_id)
    if not solicitacao:
        return None

    if solicitacao_data.status is not None:
        solicitacao.status = solicitacao_data.status

    db.commit()
    db.refresh(solicitacao)
    return solicitacao

def deletar_solicitacao(db: Session, solicitacao_id: int, usuario_id: int) -> bool:
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id, usuario_id)
    if not solicitacao:
        return False

    db.delete(solicitacao)
    db.commit()
    return True

def listar_solicitacoes_para_gestores(db: Session) -> List[SolicitacaoLaboratorio]:
    return (
        db.query(SolicitacaoLaboratorio)
        .order_by(SolicitacaoLaboratorio.criado_em.desc())
        .all()
    )
