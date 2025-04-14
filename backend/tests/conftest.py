# tests/conftest.py
import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Garante que 'app' seja encontrado como módulo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.db.base import Base

# Engine do banco de testes
engine_test = create_engine(settings.TEST_DATABASE_URL)

# Sessão de testes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# Cria as tabelas antes da sessão de testes
@pytest.fixture(scope="session", autouse=True)
def criar_tabelas():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)
