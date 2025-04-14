# backend/app/models/usuario.py

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    codigo_funcionario = Column(Integer, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)  # <-- ADICIONE ESTA LINHA
    hashed_password = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
