from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.ordem_compra import OrdemCompra
from app.models.usuario import Usuario

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/ordens-compra")
def listar_ordens_com_solicitantes(db: Session = Depends(get_db)):
    ordens = db.query(OrdemCompra).all()
    resultado = []

    for ordem in ordens:
        resultado.append({
            "id": ordem.id,
            "status": ordem.status,
            "solicitante_id": ordem.solicitante_id,
            "solicitante_nome": ordem.solicitante.nome if ordem.solicitante else None
        })

    return resultado
