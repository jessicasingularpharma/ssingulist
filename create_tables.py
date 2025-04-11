# backend/create_tables.py

# ⚠️ Esse import precisa acontecer para que os models sejam registrados corretamente
import app.models  # Garante que todos os modelos (inclusive OrdemCompra) sejam carregados
from app.db.base import Base
from app.db.database import engine

print("🔍 Verificando tabelas registradas no metadata:")
print(list(Base.metadata.tables.keys()))  # Deve mostrar todas as tabelas como usuarios, solicitacoes, ordem_compra, etc.

# Criar as tabelas no banco
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
print("📦 Tabelas finais registradas:")
for tabela in Base.metadata.sorted_tables:
    print(f" - {tabela.name}")
print("🔍 Verificando tabelas registradas no metadata:")