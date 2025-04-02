from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.auth_handler import criar_token_acesso, verificar_senha
from app.services.usuario_service import buscar_usuario_por_codigo
from app.auth.auth_bearer import get_current_user
from app.schemas.usuario import UsuarioLogin, UsuarioOut
from app.models.usuario import Usuario

router = APIRouter(tags=["Autenticação"])


@router.post("/login")
def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = buscar_usuario_por_codigo(db, login_data.codigo_funcionario)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado no sistema"
        )

    if not verificar_senha(login_data.senha, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha inválida"
        )

    token = criar_token_acesso({"sub": str(usuario.codigo_funcionario)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/usuarios/me", response_model=UsuarioOut)
def get_me(usuario: Usuario = Depends(get_current_user)):
    return usuario
