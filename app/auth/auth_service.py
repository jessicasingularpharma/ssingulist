from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.models.usuario import Usuario


def criar_token(usuario: Usuario):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"sub": str(usuario.id), "is_admin": usuario.is_admin, "exp": expire}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
