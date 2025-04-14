# backend/app/integration/firebird/erp_client.py

from app.integration.firebird.connection import get_firebird_connection


def verificar_funcionario_firebird(codigo_funcionario: int) -> dict | None:
    query = f"""
        SELECT CDFUN, NOMEFUN
        FROM FC08000
        WHERE CDFUN = {codigo_funcionario}
          AND FUNATIVO = 'S'
    """

    conn = get_firebird_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    if row:
        return {
            "CDFUN": row[0],
            "NOMEFUN": row[1],
        }

    return None
