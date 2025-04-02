# Criar estrutura de integração com Firebird para estoque com consultas diretas
from app.integration.firebird.connection import get_firebird_connection

def buscar_estoque():
    conn = get_firebird_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM FC03100")  # Exemplo: estoque por filial
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

from pathlib import Path

base = Path("/mnt/data/backend/app/integration/firebird")
base.mkdir(parents=True, exist_ok=True)

# Estoque service com consultas SQL (estrutura inicial)
estoque_service = base / "estoque_service.py"
estoque_service.write_text("""
import os
import pyodbc

def get_firebird_connection():
    conn_str = (
        f"DRIVER=Firebird/InterBase(r) driver;"
        f"UID={os.getenv('FIREBIRD_USER')};"
        f"PWD={os.getenv('FIREBIRD_PASSWORD')};"
        f"DBNAME={os.getenv('FIREBIRD_HOST')}:{os.getenv('FIREBIRD_DATABASE')};"
        f"CHARSET=UTF8"
    )
    return pyodbc.connect(conn_str)


def buscar_produtos_por_nome(nome: str, filial: int = 1):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
    SELECT
        p.CDPRO,
        p.DESCRPRD,
        p.UNIDA,
        p.CURVA,
        e.ESTAT,
        e.ESTMI,
        e.ESTMA
    FROM FC03000 p
    JOIN FC03100 e ON p.CDPRO = e.CDPRO
    WHERE e.CDFIL = ? AND p.DESCRPRD CONTAINING ?
    '''

    cursor.execute(query, (filial, nome))
    results = cursor.fetchall()
    conn.close()

    produtos = []
    for row in results:
        produtos.append({
            "cdpro": row[0],
            "descricao": row[1],
            "unidade": row[2],
            "curva": row[3],
            "estoque_atual": row[4],
            "estoque_min": row[5],
            "estoque_max": row[6],
        })
    return produtos

def buscar_lotes_por_produto(cdpro: int, filial: int = 1):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
    SELECT
        NRLOT, DTVAL, ESTAT, TEOR, DILUI, DENSI
    FROM FC03140
    WHERE CDFIL = ? AND CDPRO = ?
    '''

    cursor.execute(query, (filial, cdpro))
    results = cursor.fetchall()
    conn.close()

    lotes = []
    for row in results:
        lotes.append({
            "lote": row[0],
            "validade": row[1],
            "estoque": row[2],
            "teor": row[3],
            "diluicao": row[4],
            "densidade": row[5],
        })
    return lotes
""")
