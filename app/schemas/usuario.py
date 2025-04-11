# backend/app/schemas/usuario.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioRegistro(BaseModel):
    nome: str
    email: EmailStr
    is_admin: Optional[bool] = False


class UsuarioCreate(UsuarioRegistro):
    codigo_funcionario: int
    senha: str


class UsuarioOut(BaseModel):
    id: int
    codigo_funcionario: int
    nome: str
    email: Optional[EmailStr] = None
    is_admin: bool
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2


class UsuarioLogin(BaseModel):
    codigo_funcionario: int
    senha: str


class UsuarioRegistroResponse(BaseModel):
    mensagem: str
    senha_gerada: str


class AlterarSenhaRequest(BaseModel):
    senha_atual: str = Field(..., min_length=4)
    nova_senha: str = Field(..., min_length=4)


class AlterarSenhaInput(BaseModel):
    nova_senha: str
