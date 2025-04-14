from fastapi import APIRouter

router = APIRouter(prefix="/minhas-solicitacoes", tags=["Minhas Solicitações"])


@router.get("")
def teste():
    return {"ok": True}
