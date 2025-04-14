# app/schemas/franquia_ordem.py

from datetime import date

from pydantic import BaseModel, Field


class FranquiaOrdemCreate(BaseModel):
    ordem_id: int = Field(..., description="ID da ordem de compra")
    unidade_franquia: str = Field(
        ..., description="Nome ou código da unidade de franquia"
    )
    data_compra: date = Field(..., description="Data da compra feita pela franquia")
    item: str = Field(..., description="Nome do item comprado pela franquia")
    quantidade: int = Field(..., description="Quantidade comprada")
    unidade: str = Field(..., description="Unidade de medida")


class FranquiaOrdemOut(FranquiaOrdemCreate):
    id: int

    class Config:
        from_attributes = True
