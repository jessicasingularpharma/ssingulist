# backend/app/routers/produto.py

import firebirdsql
from fastapi import APIRouter, HTTPException, Query

from app.integration.firebird_db.connection import get_firebird_connection

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/buscar")
def buscar_produtos(nome: str = Query(..., min_length=2)):
    try:
        conn = get_firebird_connection()
        cur = conn.cursor()

        query = """
        SELECT FIRST 10 CDPRO, DESCR, UNIDA
        FROM FC03000
        WHERE DESCR CONTAINING ?
          AND INDDEL = 'N'
        ORDER BY DESCR
        """

        cur.execute(query, (nome,))
        resultados = cur.fetchall()
        conn.close()

        return [
            {
                "codigo": row[0],
                "descricao": row[1].strip(),
                "unidade": row[2].strip() if row[2] else "",
            }
            for row in resultados
        ]

    except firebirdsql.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao consultar produtos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
