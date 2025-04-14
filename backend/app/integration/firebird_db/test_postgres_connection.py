import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carrega variáveis do .env
load_dotenv()

# Monta a URL de conexão
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Cria engine SQLAlchemy
engine = create_engine(DATABASE_URL)


def testar_conexao_postgres():
    try:
        with engine.connect() as conn:
            resultado = conn.execute(text("SELECT version();"))
            versao = resultado.fetchone()[0]
            print("✅ Conectado ao PostgreSQL com sucesso:")
            print("📦 Versão do PostgreSQL:", versao)
    except Exception as e:
        print("❌ Erro ao conectar ao PostgreSQL:", e)


if __name__ == "__main__":
    testar_conexao_postgres()
