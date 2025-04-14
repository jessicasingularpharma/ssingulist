# app/schemas/pendencia_substancia.py

from typing import Literal

from pydantic import BaseModel, Field


class PendenciaSubstanciaCreate(BaseModel):
    ordem_id: int = Field(..., description="ID da ordem de compra")
    situacao: str = Field(
        ..., description="Situação da substância (ex: falta de estoque)"
    )
    localizacao: str = Field(
        ..., description="Localização física ou de processo da substância"
    )
    status: Literal["ok", "processando", "encerrada"] = Field(
        ..., description="Status da pendência"
    )


class PendenciaSubstanciaOut(PendenciaSubstanciaCreate):
    id: int

    class Config:
        from_attributes = True
