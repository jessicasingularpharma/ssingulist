from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import enum
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# --- ENUM ---
class StatusOrdemCompra(str, enum.Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    em_pendencia = "em_pendencia"
    concluido = "concluido"


# --- MODELS SQLAlchemy ---

class OrdemCompra(Base):
    __tablename__ = "ordens_compra"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String, unique=True, index=True)  # ✅ Novo campo
    solicitante_id = Column(Integer, ForeignKey("singulist.usuarios.id"), nullable=False)

    status = Column(Enum(StatusOrdemCompra), nullable=False, default=StatusOrdemCompra.aberto)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    solicitante = relationship("Usuario", back_populates="ordens_compra")
    itens = relationship("OrdemCompraItem", back_populates="ordem", cascade="all, delete")
    detalhes = relationship("OrdemCompraDetalhes", back_populates="ordem", uselist=False, cascade="all, delete")
    pendencias_substancias = relationship("PendenciaSubstancia", back_populates="ordem", cascade="all, delete")
    franquias = relationship("FranquiaOrdem", back_populates="ordem", cascade="all, delete")
    historico_status = relationship("OrdemCompraStatusHistorico", back_populates="ordem", cascade="all, delete")

class OrdemCompraStatusHistorico(Base):
    __tablename__ = "ordens_compra_status_historico"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    status = Column(Enum(StatusOrdemCompra), nullable=False)
    alterado_por = Column(Integer, ForeignKey("singulist.usuarios.id"), nullable=False)
    data_alteracao = Column(DateTime(timezone=True), server_default=func.now())

    ordem = relationship("OrdemCompra", back_populates="historico_status")
    usuario = relationship("Usuario")


class OrdemCompraItem(Base):
    __tablename__ = "ordens_compra_itens"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)

    codigo_produto = Column(Integer, nullable=False)
    nome_produto = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    unidade = Column(String, nullable=True)
    observacao = Column(String, nullable=True)
    data_necessidade = Column(Date, nullable=True)
    urgente = Column(Boolean, default=False)

    ordem = relationship("OrdemCompra", back_populates="itens")


class OrdemCompraDetalhes(Base):
    __tablename__ = "ordens_compra_detalhes"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False, unique=True)
    data_compra = Column(Date, nullable=True)
    previsao_chegada = Column(Date, nullable=True)
    fornecedor = Column(String, nullable=True)
    observacao_geral = Column(Text, nullable=True)

    ordem = relationship("OrdemCompra", back_populates="detalhes")


class PendenciaSubstancia(Base):
    __tablename__ = "pendencias_substancias"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    situacao = Column(String, nullable=False)
    localizacao = Column(String, nullable=True)
    status = Column(String, nullable=False)

    ordem = relationship("OrdemCompra", back_populates="pendencias_substancias")


class FranquiaOrdem(Base):
    __tablename__ = "franquias_ordens"
    __table_args__ = {"schema": "singulist"}

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey("singulist.ordens_compra.id"), nullable=False)
    unidade_franquia = Column(String, nullable=False)
    data_compra = Column(Date, nullable=True)
    item = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    unidade = Column(String, nullable=True)

    ordem = relationship("OrdemCompra", back_populates="franquias")


# --- SCHEMAS Pydantic ---

# Enum para os status
StatusOrdemCompraLiteral = Literal[
    "aberto",
    "em_andamento",
    "em_pendencia",
    "concluido"
]

# Schema para atualizar o status da ordem
class OrdemCompraStatusUpdate(BaseModel):
    status: StatusOrdemCompraLiteral

    class Config:
        from_attributes = True

# Schema de histórico de status (entrada)
class OrdemCompraStatusHistoricoCreate(BaseModel):
    ordem_id: int
    status: StatusOrdemCompraLiteral
    alterado_por: int

# Schema de histórico de status (saída)
class OrdemCompraStatusHistoricoOut(BaseModel):
    id: int
    ordem_id: int
    status: StatusOrdemCompraLiteral
    alterado_por: int
    data_alteracao: datetime

    class Config:
        from_attributes = True

# Detalhes da Ordem de Compra
class OrdemCompraDetalhesBase(BaseModel):
    data_compra: Optional[date] = Field(None, description="Data da compra")
    previsao_chegada: Optional[date] = Field(None, description="Previsão de chegada")
    fornecedor: Optional[str] = Field(None, max_length=100)
    observacao: Optional[str] = Field(None, max_length=255)

class OrdemCompraDetalhesCreate(OrdemCompraDetalhesBase):
    ordem_id: int

class OrdemCompraDetalhesOut(OrdemCompraDetalhesBase):
    id: int
    ordem_id: int
    class Config:
        from_attributes = True


# Pendências de Substâncias
class PendenciaSubstanciaBase(BaseModel):
    situacao: str = Field(..., max_length=100)
    localizacao: str = Field(..., max_length=100)
    status: str = Field(..., pattern="^(ok|processando|encerrada)$")  # 🔧 atualizado

class PendenciaSubstanciaCreate(PendenciaSubstanciaBase):
    ordem_id: int

class PendenciaSubstanciaOut(PendenciaSubstanciaBase):
    id: int
    ordem_id: int
    class Config:
        from_attributes = True


# Franquias
class FranquiaOrdemBase(BaseModel):
    unidade_franquia: str = Field(..., max_length=100)
    data_compra: date
    item: str = Field(..., max_length=100)
    quantidade: int
    unidade: str = Field(..., max_length=20)

class FranquiaOrdemCreate(FranquiaOrdemBase):
    ordem_id: int

class FranquiaOrdemOut(FranquiaOrdemBase):
    id: int
    ordem_id: int
    class Config:
        from_attributes = True
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Boolean, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
import enum

# --- ENUM ---
class StatusOrdemCompra(str, enum.Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    em_pendencia = "em_pendencia"
    concluido = "concluido"

