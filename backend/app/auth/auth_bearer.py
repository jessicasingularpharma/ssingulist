# backend/app/auth/auth_bearer.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from app.auth.auth_handler import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    codigo_funcionario = decodificar_token(token)

    if not codigo_funcionario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.query(Usuario).filter(Usuario.codigo_funcionario == int(codigo_funcionario)).first()

    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou inativo")

    return usuario
