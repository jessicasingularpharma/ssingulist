from passlib.context import CryptContext

# Inicializa o contexto de criptografia com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Gera um hash seguro da senha utilizando bcrypt.
    """
    return pwd_context.hash(password)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)
