# app/models/ordem_compra_detalhes.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class OrdemCompraDetalhes(Base):
    __tablename__ = "ordem_compra_detalhes"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    data_compra = Column(Date, nullable=True)
    previsao_chegada = Column(Date, nullable=True)
    fornecedor = Column(String, nullable=True)
    observacao = Column(String, nullable=True)

    ordem = relationship("OrdemCompra", backref="detalhes")
