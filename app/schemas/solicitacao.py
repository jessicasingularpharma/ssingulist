from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Em vez de importar no início, vamos importar diretamente dentro da função
class SolicitacaoItemCreate(BaseModel):
    codigo_produto: str
    nome_produto: str
    quantidade: str
    unidade: str


class SolicitacaoItemOut(BaseModel):
    id: int
    codigo_produto: str
    nome_produto: str
    quantidade: str
    unidade: str

    class Config:
        from_attributes = True


class SolicitacaoCreate(BaseModel):
    solicitante_id: int
    itens: List[SolicitacaoItemCreate]  # Aqui utilizamos a classe SolicitacaoItemCreate


class SolicitacaoUpdate(BaseModel):
    descricao: Optional[str] = None
    status: Optional[str] = None


class SolicitacaoOut(BaseModel):
    id: int
    status: str
    criado_em: datetime
    itens: List[SolicitacaoItemOut]  # Aqui utilizamos a classe SolicitacaoItemOut

    class Config:
        from_attributes = True
