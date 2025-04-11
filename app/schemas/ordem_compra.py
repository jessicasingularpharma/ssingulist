from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date, datetime
from app.models.ordem_compra import FranquiaOrdemOut, OrdemCompraDetalhesOut, PendenciaSubstanciaOut
from app.schemas.usuario import UsuarioOut

# --- ENUM COMPATÍVEL ---
StatusOrdemCompraLiteral = Literal["aberto", "em_andamento", "em_pendencia", "concluido"]

# --- SCHEMAS DE ITENS ---
class OrdemCompraItemCreate(BaseModel):
    codigo_produto: int
    nome_produto: str
    quantidade: int
    unidade: str
    observacao: Optional[str] = None
    data_necessidade: Optional[date] = None
    urgente: bool = False

class OrdemCompraItemOut(BaseModel):
    id: int
    codigo_produto: int
    nome_produto: str
    quantidade: int
    unidade: Optional[str]
    observacao: Optional[str]
    data_necessidade: Optional[date]
    urgente: bool

    class Config:
        from_attributes = True

# --- SCHEMA DE CRIAÇÃO DA ORDEM ---
class OrdemCompraCreate(BaseModel):
    solicitante_id: int
    itens: List[OrdemCompraItemCreate]
    data_necessidade: Optional[date] = None
    urgente: bool = False

# --- USUÁRIO SIMPLES ---
class UsuarioOutSimples(BaseModel):
    id: int
    nome: Optional[str]
    codigo_funcionario: Optional[int]

    class Config:
        from_attributes = True

# --- DETALHES DA ORDEM ---
class OrdemCompraDetalhesUpdate(BaseModel):
    data_compra: Optional[date]
    previsao_chegada: Optional[date]
    fornecedor: Optional[str]
    observacao_geral: Optional[str]

    class Config:
        from_attributes = True

# --- STATUS HISTÓRICO ---
class OrdemCompraStatusHistoricoOut(BaseModel):
    id: int
    ordem_id: int
    status: StatusOrdemCompraLiteral
    alterado_por: int
    data_alteracao: datetime

    class Config:
        from_attributes = True

class OrdemCompraStatusUpdate(BaseModel):
    status: StatusOrdemCompraLiteral

    class Config:
        from_attributes = True

# --- SAÍDA COMPLETA DA ORDEM ---
class OrdemCompraOut(BaseModel):
    id: int
    identificador: str
    solicitante_id: int
    status: StatusOrdemCompraLiteral
    criado_em: datetime
    solicitante: Optional[UsuarioOut]
    itens: List[OrdemCompraItemOut]
    detalhes: Optional[OrdemCompraDetalhesOut]
    pendencias_substancias: List[PendenciaSubstanciaOut]
    franquias: List[FranquiaOrdemOut]
    tipo: Optional[str] = "suprimentos"

    class Config:
        from_attributes = True