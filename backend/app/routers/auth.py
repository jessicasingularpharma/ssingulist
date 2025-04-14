# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth_bearer import get_current_user
from app.auth.auth_handler import criar_token_acesso
from app.core.security import verificar_senha
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin, UsuarioOut
from app.services.usuario_service import buscar_usuario_por_codigo

router = APIRouter(tags=["Autenticação"])


@router.post("/login")
def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = buscar_usuario_por_codigo(db, login_data.codigo_funcionario)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    if not verificar_senha(login_data.senha, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha inválida"
        )

    # 👇 Aqui o print pra te ajudar a ver se é admin
    print(f"🔐 Usuário autenticado: {usuario.nome} | Admin: {usuario.is_admin}")

    # Gera token com sub e is_admin
    token = criar_token_acesso(usuario)
    return {"access_token": token, "token_type": "bearer"}
