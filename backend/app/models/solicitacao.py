from sqlalchemy import Column, Integer, String, DateTime,func
from app.db.database import Base

class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome_solicitante = Column(String, index=True)
    descricao = Column(String, nullable=False)
    status = Column(String, default="Pendente", nullable=False)
    created_at = Column(DateTime (timezone=True), server_default=func.now()) 
