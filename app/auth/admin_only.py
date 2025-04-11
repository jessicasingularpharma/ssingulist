from app.auth.auth_bearer import get_current_user
from app.models.usuario import Usuario
from fastapi import Depends, HTTPException, status


def verificar_admin(usuario: Usuario = Depends(get_current_user)):
    if not usuario.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores.",
        )
    return usuario
