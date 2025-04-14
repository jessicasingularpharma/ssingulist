# backend/app/schemas/usuario.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Schema de entrada (cadastro, login)
class UsuarioCreate(BaseModel):
    codigo_funcionario: int
    nome: str
    email: Optional[EmailStr] = None
    senha: str


# Schema de saída (dados públicos)
class UsuarioOut(BaseModel):
    id: int
    codigo_funcionario: int
    nome: str
    email: Optional[EmailStr] = None
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True  # Usado no lugar do antigo orm_mode


# Schema básico para login
class UsuarioLogin(BaseModel):
    codigo_funcionario: int
    senha: str
