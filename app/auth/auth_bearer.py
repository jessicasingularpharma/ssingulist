# backend/app/auth/auth_bearer.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.auth_handler import decodificar_token
from app.db.database import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    payload = decodificar_token(token)

    if not payload or "codigo_funcionario" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        codigo_funcionario = int(payload["codigo_funcionario"])
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de funcionário inválido no token.",
        )

    usuario = (
        db.query(Usuario)
        .filter(Usuario.codigo_funcionario == codigo_funcionario)
        .first()
    )

    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou inativo")

    print(f"🔐 Usuário autenticado: {usuario.nome} | Admin: {usuario.is_admin}")
    return usuario
