# backend/app/routers/usuario.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services.usuario_service import (buscar_usuario_por_codigo,
                                          criar_usuario)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se já existe
    usuario_existente = buscar_usuario_por_codigo(db, usuario.codigo_funcionario)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")

    novo_usuario = criar_usuario(db, usuario)
    return novo_usuario
