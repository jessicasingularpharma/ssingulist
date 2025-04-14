from sqlalchemy.orm import Session

from app.models.solicitacao import Solicitacao
from app.schemas.solicitacao import SolicitacaoCreate


def create_solicitacao(db: Session, solicitacao: SolicitacaoCreate):
    nova = Solicitacao(**solicitacao.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def listar_solicitacoes(db: Session):
    return db.query(Solicitacao).all()


def buscar_solicitacao(db: Session, solicitacao_id: int):
    return db.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
