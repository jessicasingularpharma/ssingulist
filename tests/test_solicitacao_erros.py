import random
from datetime import datetime

import pytest
from app.auth.auth_handler import criar_token_acesso
from app.db.database import get_db
from app.main import app
from app.models.usuario import Usuario
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

client = TestClient(app)


# Fixture de sessão de banco (ajuste se estiver usando override)
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db
    db.close()


# Fixture de usuário autenticado com código aleatório
@pytest.fixture
def usuario_autenticado(db_session: Session):
    codigo = random.randint(100000, 999999)
    usuario = Usuario(
        codigo_funcionario=codigo,
        nome="Usuário Teste",
        email=f"teste{codigo}@empresa.com",
        hashed_password="senha123",
        ativo=True,
        criado_em=datetime.utcnow(),
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    token = criar_token_acesso({"sub": str(usuario.codigo_funcionario)})
    headers = {"Authorization": f"Bearer {token}"}
    return usuario, headers


def test_criar_solicitacao_payload_invalido(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.post("/solicitacoes/", json={}, headers=headers)
    assert response.status_code == 422  # campo obrigatório faltando


def test_buscar_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.get("/solicitacoes/999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"


def test_atualizar_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    payload = {"descricao": "Teste", "status": "pendente"}
    response = client.put("/solicitacoes/999999", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"


def test_deletar_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.delete("/solicitacoes/999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"
