# backend/app/models/usuario.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "singulist"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo_funcionario = Column(Integer, unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
