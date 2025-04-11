from .solicitacao import SolicitacaoLaboratorio  # noqa: F401
from .usuario import Usuario  # noqa: F401
# backend/app/models/__init__.py

from .usuario import Usuario
from .solicitacao import SolicitacaoLaboratorio  # noqa: F401
from .ordem_compra import OrdemCompra, OrdemCompraItem  # 👈 ADICIONE ESTA LINHA
