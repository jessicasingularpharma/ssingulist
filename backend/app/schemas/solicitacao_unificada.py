from typing import List

from pydantic import BaseModel

from app.schemas.ordem_compra import OrdemCompraOut
from app.schemas.solicitacao import SolicitacaoOut


class MinhasSolicitacoesResponse(BaseModel):
    ordens_compra: List[OrdemCompraOut]
    solicitacoes_laboratorio: List[SolicitacaoOut]

    class Config:
        from_attributes = True
