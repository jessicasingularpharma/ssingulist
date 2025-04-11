from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    codigo_funcionario = Column(Integer, unique=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    ordens_compra = relationship("OrdemCompra", back_populates="solicitante")  # Para ordens de compra
    solicitacoes_lab = relationship("SolicitacaoLaboratorio", back_populates="solicitante")  # Para solicitações do laboratório
