from app.integration.firebird_db.connection import get_firebird_connection

def buscar_produtos_por_nome(nome: str):
    conn = get_firebird_connection()
    cursor = conn.cursor()

    query = """
        SELECT FIRST 10 CDPRO, DESCR, UNIDA
        FROM FC03000
        WHERE DESCR CONTAINING ?
        ORDER BY DESCR
    """
    cursor.execute(query, (nome,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {"codigo": row[0], "descricao": row[1], "unidade": row[2]}
        for row in rows
    ]
