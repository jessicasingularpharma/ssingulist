# backend/app/routers/minhas_solicitacoes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.solicitacao_unificada import MinhasSolicitacoesResponse
from app.services.ordem_compra_service import listar_ordens_por_usuario
from app.services.solicitacao_service import listar_solicitacoes_por_usuario

router = APIRouter(prefix="/minhas-solicitacoes", tags=["Solicitações"])


@router.get("/", response_model=MinhasSolicitacoesResponse)
def obter_minhas_solicitacoes(
    db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    ordens = listar_ordens_por_usuario(db, usuario.id)
    solicitacoes = listar_solicitacoes_por_usuario(db, usuario.id)
    return {"ordens_compra": ordens, "solicitacoes_laboratorio": solicitacoes}
