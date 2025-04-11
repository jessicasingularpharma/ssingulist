from app.auth.auth_bearer import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import AlterarSenhaInput, UsuarioOut, UsuarioRegistro
from app.services.usuario_service import alterar_senha, registrar_usuario
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return db.query(Usuario).all()

@router.get("/me", response_model=UsuarioOut)
def get_me(usuario: Usuario = Depends(get_current_user)):
    return usuario

@router.post("/registrar", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(
    dados: UsuarioRegistro,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Ou remova esse Depends para permitir registro sem login
):
    existente = db.query(Usuario).filter(Usuario.codigo_funcionario == dados.codigo_funcionario).first()
    if existente:
        raise HTTPException(status_code=400, detail="Usuário já registrado")

    return registrar_usuario(db, dados)

@router.put("/alterar-senha", status_code=status.HTTP_204_NO_CONTENT)
def alterar_senha_endpoint(
    dados: AlterarSenhaInput,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    alterar_senha(db, usuario.id, dados.senha_atual, dados.nova_senha)
    return None