# ✅ MODELS - backend/app/models/solicitacao_laboratorio.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class SolicitacaoLaboratorio(Base):
    __tablename__ = "solicitacoes_laboratorio"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    solicitante_id = Column(Integer, ForeignKey("singulist.usuarios.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="aberto", nullable=False)

    solicitante = relationship("Usuario", back_populates="solicitacoes_laboratorio")
    itens = relationship("SolicitacaoLaboratorioItem", back_populates="solicitacao", cascade="all, delete")
    historico_status = relationship("SolicitacaoLaboratorioStatusHistorico", back_populates="solicitacao", cascade="all, delete")

class SolicitacaoLaboratorioItem(Base):
    __tablename__ = "solicitacoes_laboratorio_itens"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True)
    solicitacao_id = Column(Integer, ForeignKey("singulist.solicitacoes_laboratorio.id"), nullable=False)
    codigo_produto = Column(Integer, nullable=False)
    nome_produto = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    unidade = Column(String)
    observacao = Column(String)
    data_necessidade = Column(Date)
    urgente = Column(Boolean, default=False)

    solicitacao = relationship("SolicitacaoLaboratorio", back_populates="itens")

class SolicitacaoLaboratorioStatusHistorico(Base):
    __tablename__ = "solicitacoes_laboratorio_status_historico"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True)
    solicitacao_id = Column(Integer, ForeignKey("singulist.solicitacoes_laboratorio.id"))
    status = Column(String, nullable=False)
    alterado_por = Column(Integer, ForeignKey("singulist.usuarios.id"))
    data_alteracao = Column(DateTime(timezone=True), server_default=func.now())

    solicitacao = relationship("SolicitacaoLaboratorio", back_populates="historico_status")
    usuario = relationship("Usuario")
