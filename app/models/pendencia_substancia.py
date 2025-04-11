# app/models/pendencia_substancia.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class PendenciaSubstancia(Base):
    __tablename__ = "pendencias_substancias"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    situacao = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    status = Column(String, nullable=False)  # ok, processando, encerrada

    ordem = relationship("OrdemCompra", backref="pendencias_substancias")
