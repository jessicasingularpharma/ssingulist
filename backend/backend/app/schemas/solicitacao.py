from datetime import datetime

from pydantic import BaseModel


class SolicitacaoCreate(BaseModel):
    descricao: str


class SolicitacaoOut(BaseModel):
    id: int
    descricao: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
