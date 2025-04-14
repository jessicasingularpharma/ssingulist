# backend/app/integration/firebird_db/firebird.py

import firebirdsql

from app.core.config import settings


def buscar_funcionario_por_nome(nome: str):
    con = firebirdsql.connect(
        host=settings.firebird_host,
        database=settings.firebird_database,
        user=settings.firebird_user,
        password=settings.firebird_password,
        charset="ISO8859_1",
    )

    cur = con.cursor()
    cur.execute("SELECT CDFUN FROM FC08000 WHERE NOMEFUN = ?", (nome.strip(),))
    resultado = cur.fetchone()
    con.close()

    return resultado[0] if resultado else None


# backend/app/integration/firebird_db/firebird.py
from app.integration.firebird_db.connection import get_firebird_connection


def buscar_produtos_por_nome(nome: str):
    conn = get_firebird_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT FIRST 10 CDPRO, DESCR, UNIDA
        FROM FC03000
        WHERE DESCR CONTAINING ?
        ORDER BY DESCR
    """

    cursor.execute(query, (nome,))
    resultados = cursor.fetchall()

    produtos = [
        {"codigo": row[0], "descricao": row[1].strip(), "unidade": row[2].strip()}
        for row in resultados
    ]

    cursor.close()
    conn.close()
    return produtos
