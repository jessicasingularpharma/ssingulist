import random

import pytest
from app.auth.auth_handler import criar_token_acesso
from app.db.database import SessionLocal
from app.main import app
from app.models.usuario import Usuario
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

client = TestClient(app)


@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def usuario_autenticado(db_session: Session):
    usuario = Usuario(
        codigo_funcionario=999999,
        nome="Usuário Teste",
        email="teste@empresa.com",
        hashed_password="senha123",
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    token = criar_token_acesso(usuario.codigo_funcionario)  # <- importante!
    headers = {"Authorization": f"Bearer {token}"}
    return usuario, headers


def test_criar_solicitacao_payload_invalido(usuario_autenticado):
    _, headers = usuario_autenticado

    # Payload vazio: falta o campo obrigatório 'descricao'
    response = client.post("/solicitacoes/", json={}, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 422  # Unprocessable Entity


def test_criar_solicitacao_sem_autenticacao():
    payload = {"descricao": "Item sem token"}
    response = client.post("/solicitacoes/", json=payload)
    assert response.status_code == 401


def test_obter_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.get("/solicitacoes/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"


def test_atualizar_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    update = {"descricao": "Nova descrição"}
    response = client.put("/solicitacoes/9999", json=update, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"


def test_deletar_solicitacao_inexistente(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.delete("/solicitacoes/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitação não encontrada"


def test_listar_solicitacoes_sem_token():
    response = client.get("/solicitacoes/")
    assert response.status_code == 401
