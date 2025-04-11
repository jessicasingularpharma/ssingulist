# backend/app/auth/auth_firebird.py

import os

import firebirdsql
from dotenv import load_dotenv

load_dotenv()


def verificar_funcionario_firebird(codigo_funcionario: int):
    """
    Verifica se o funcionário existe e está ativo no banco Firebird.
    Retorna o nome e o e-mail se encontrado e ativo.
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
        cur = conn.cursor()
        query = """
            SELECT NOMEFUN, EMAIL, FUNATIVO
            FROM FC08000
            WHERE CDFUN = ?
        """
        cur.execute(query, (codigo_funcionario,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            nome, email, ativo = result
            if ativo == "S":
                return {"nome": nome, "email": email}
        return None

    except Exception as e:
        print(f"❌ Erro ao consultar funcionário no Firebird: {e}")
        return None
