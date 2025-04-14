# backend/app/services/auth_handler.py

from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.models.usuario import Usuario

# Configurações do token
SECRET_KEY = settings.SECRET_KEY or "secret"
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES or 1440  # 24 horas


def criar_token_acesso(usuario: Usuario) -> str:
    """
    Gera um token JWT contendo o código do funcionário e se ele é admin.

    Args:
        usuario (Usuario): Usuário autenticado.

    Returns:
        str: Token JWT gerado.
    """
    to_encode = {
        "sub": str(usuario.codigo_funcionario),
        "is_admin": bool(usuario.is_admin),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str):
    """
    Decodifica um token JWT e retorna os dados contidos nele.

    Args:
        token (str): Token JWT.

    Returns:
        dict | None: Payload decodificado ou None se inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
