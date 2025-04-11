# app/db/session.py

from typing import Generator

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Monta a string de conexão com o PostgreSQL
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

# Cria o engine do SQLAlchemy com verificação de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
