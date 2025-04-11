from pydantic import BaseModel
from typing import List
from app.schemas.ordem_compra import OrdemCompraOut
from app.schemas.solicitacao import SolicitacaoOut


class MinhasSolicitacoesResponse(BaseModel):
    ordens_compra: List[OrdemCompraOut]
    solicitacoes_laboratorio: List[SolicitacaoOut]

    class Config:
        from_attributes = True
