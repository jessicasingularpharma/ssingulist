from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.solicitacao import SolicitacaoCreate, SolicitacaoOut
from app.services import solicitacao

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações"])


@router.post("/", response_model=SolicitacaoOut)
def criar(solicitacao: SolicitacaoCreate, db: Session = Depends(get_db)):
    return solicitacao.create_solicitacao(db, solicitacao)


@router.get("/", response_model=list[SolicitacaoOut])
def listar(db: Session = Depends(get_db)):
    return solicitacao.listar_solicitacoes(db)


@router.get("/{solicitacao_id}", response_model=SolicitacaoOut)
def obter(solicitacao_id: int, db: Session = Depends(get_db)):
    solicitacao = solicitacao.buscar_solicitacao(db, solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return solicitacao
