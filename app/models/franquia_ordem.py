# app/models/franquia_ordem.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class FranquiaOrdem(Base):
    __tablename__ = "franquias_ordens"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    unidade_franquia = Column(String, nullable=False)
    data_compra = Column(Date, nullable=False)
    item = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    unidade = Column(String, nullable=False)

    ordem = relationship("OrdemCompra", backref="franquias")
