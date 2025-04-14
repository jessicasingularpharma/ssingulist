# backend/app/db/create_tables.py

from sqlalchemy import text

from app.db.database import Base, engine
from app.models.usuario import Usuario

print("Verificando schema...")
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS singulist;"))
    conn.commit()

print("Criando tabelas no schema singulist...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso.")
