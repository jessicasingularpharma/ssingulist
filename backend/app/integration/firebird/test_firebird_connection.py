import os
import firebirdsql
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    """Conecta ao banco de dados Firebird usando firebirdsql."""
    try:
        return firebirdsql.connect(
            host=os.getenv("FIREBIRD_HOST"),
            database=os.getenv("FIREBIRD_DATABASE").replace("\\", "/"),
            port=3050,
            user=os.getenv("FIREBIRD_USER"),
            password=os.getenv("FIREBIRD_PASSWORD"),
            charset="WIN1252"
        )
    except Exception as e:
        raise ConnectionError(f"❌ Erro ao conectar ao Firebird: {e}")

def testar_conexao():
    try:
        conn = conectar_banco()
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_DATE FROM RDB$DATABASE")
        data = cur.fetchone()[0]
        print("✅ Conectado ao Firebird. Data atual:", data)
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    testar_conexao()
