# ✅ SCHEMAS - backend/app/schemas/solicitacao_laboratorio.py
from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import date, datetime

class SolicitacaoLaboratorioItemCreate(BaseModel):
    codigo_produto: int
    nome_produto: str
    quantidade: int
    unidade: str
    observacao: Optional[str] = None
    data_necessidade: Optional[date] = None
    urgente: bool = False

class SolicitacaoLaboratorioCreate(BaseModel):
    
    itens: List[SolicitacaoLaboratorioItemCreate]

class SolicitacaoLaboratorioStatusHistoricoOut(BaseModel):
    id: int
    solicitacao_id: int
    status: str
    alterado_por: int
    data_alteracao: datetime

    class Config:
        from_attributes = True

class SolicitacaoLaboratorioItemOut(SolicitacaoLaboratorioItemCreate):
    id: int

    class Config:
        from_attributes = True

class SolicitacaoLaboratorioOut(BaseModel):
    id: int
    solicitante_id: int
    status: str
    criado_em: datetime
    itens: List[SolicitacaoLaboratorioItemOut]
    historico_status: List[SolicitacaoLaboratorioStatusHistoricoOut]

    class Config:
        from_attributes = True

StatusLaboratorioLiteral = Literal["aberto", "em_andamento", "em_pendencia", "concluido"]

class SolicitacaoLaboratorioStatusUpdate(BaseModel):
    status: StatusLaboratorioLiteral

    class Config:
        from_attributes = True