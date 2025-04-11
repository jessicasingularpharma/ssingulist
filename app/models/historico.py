# backend/app/models/historico.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class HistoricoSolicitacao(Base):
    __tablename__ = "historico_solicitacao"

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"), nullable=False)
    tipo = Column(String, nullable=False)  # "laboratorio" ou "ordem_compra"
    status_anterior = Column(String, nullable=True)
    status_novo = Column(String, nullable=False)
    atualizado_por = Column(String, nullable=True)
    data_alteracao = Column(DateTime, default=datetime.utcnow)

    solicitacao = relationship("Solicitacao", back_populates="historicos")
