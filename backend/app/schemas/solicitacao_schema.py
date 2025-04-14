from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class SolicitacaoCreate(BaseModel):
    produto_id: int = Field(..., description="ID do produto solicitado")
    quantidade: int = Field(
        ..., gt=0, description="Quantidade do produto a ser solicitada"
    )
    observacao: Optional[str] = Field(
        None, max_length=255, description="Observações adicionais da solicitação"
    )


class SolicitacaoUpdate(BaseModel):
    quantidade: Optional[int] = Field(
        None, gt=0, description="Quantidade atualizada do produto"
    )
    observacao: Optional[str] = Field(
        None, max_length=255, description="Nova observação da solicitação"
    )
    status: Optional[str] = Field(
        None, description="Status da solicitação (ex: pendente, aprovado, rejeitado)"
    )


class SolicitacaoOut(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    observacao: Optional[str]
    status: str
    usuario_id: int
    data_criacao: date

    class Config:
        from_attributes = True
