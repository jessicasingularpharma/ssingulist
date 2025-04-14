from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class SolicitacaoLaboratorio(Base):
    __tablename__ = "solicitacoes_laboratorio"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    solicitante_id = Column(
        Integer, ForeignKey("singulist.usuarios.id"), nullable=False
    )
    criado_em = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="em_andamento")

    solicitante = relationship("Usuario", back_populates="solicitacoes_lab")
    itens = relationship(
        "SolicitacaoItem", back_populates="solicitacao", cascade="all, delete-orphan"
    )


class SolicitacaoItem(Base):
    __tablename__ = "solicitacoes_laboratorio_itens"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(
        Integer, ForeignKey("singulist.solicitacoes_laboratorio.id"), nullable=False
    )
    codigo_produto = Column(String)
    nome_produto = Column(String)
    quantidade = Column(String)
    unidade = Column(String)

    solicitacao = relationship("SolicitacaoLaboratorio", back_populates="itens")
