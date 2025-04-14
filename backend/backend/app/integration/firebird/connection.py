import os

import firebirdsql
from dotenv import load_dotenv

load_dotenv()


def get_firebird_connection():
    """
    Retorna uma conexão ativa com o banco Firebird usando as variáveis de ambiente.
    Essa função deve ser utilizada em qualquer módulo que precise acessar dados do ERP.
    """
    try:
        conn = firebirdsql.connect(
            host=os.getenv("FIREBIRD_HOST"),
            database=os.getenv("FIREBIRD_DATABASE").replace("\\", "/"),
            port=3050,
            user=os.getenv("FIREBIRD_USER"),
            password=os.getenv("FIREBIRD_PASSWORD"),
            charset="WIN1252",
        )
        return conn
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar ao Firebird: {e}")
