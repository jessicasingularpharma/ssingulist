from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class OrdemCompraDetalhesCreate(BaseModel):
    ordem_id: int = Field(..., description="ID da ordem de compra")
    data_compra: Optional[date] = Field(None, description="Data em que a compra foi realizada")
    previsao_chegada: Optional[date] = Field(None, description="Previsão de chegada dos produtos")
    fornecedor: Optional[str] = Field(None, description="Nome do fornecedor")
    observacao: Optional[str] = Field(None, description="Observações adicionais")  # ✅ nome corrigido

class OrdemCompraDetalhesOut(BaseModel):
    id: int
    data_compra: Optional[date]
    previsao_chegada: Optional[date]
    fornecedor: Optional[str]
    observacao: Optional[str]  # ✅ nome corrigido

    class Config:
        from_attributes = True
