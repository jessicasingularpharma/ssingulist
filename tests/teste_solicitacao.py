import pytest
from app.db.database import SessionLocal, get_db
from app.main import app
from app.models.usuario import Usuario
from app.services.auth_handler import criar_token_jwt
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
        codigo_funcionario=9,
        nome="Usuário Teste",
        email="teste@empresa.com",
        hashed_password="senha123",
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    token = criar_token_jwt(usuario.id)
    headers = {"Authorization": f"Bearer {token}"}
    return usuario, headers


def test_criar_solicitacao(usuario_autenticado):
    _, headers = usuario_autenticado
    payload = {"descricao": "Comprar materiais de limpeza"}

    response = client.post("/solicitacoes/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["descricao"] == payload["descricao"]


def test_listar_solicitacoes(usuario_autenticado):
    _, headers = usuario_autenticado

    response = client.get("/solicitacoes/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obter_solicitacao(usuario_autenticado):
    _, headers = usuario_autenticado
    # Primeiro cria
    response_criar = client.post(
        "/solicitacoes/", json={"descricao": "Cabo HDMI"}, headers=headers
    )
    solicitacao_id = response_criar.json()["id"]

    # Depois busca
    response_buscar = client.get(f"/solicitacoes/{solicitacao_id}", headers=headers)
    assert response_buscar.status_code == 200
    assert response_buscar.json()["descricao"] == "Cabo HDMI"


def test_atualizar_solicitacao(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.post(
        "/solicitacoes/", json={"descricao": "Item para editar"}, headers=headers
    )
    solicitacao_id = response.json()["id"]

    update = {"descricao": "Item atualizado", "status": "aprovado"}
    response_update = client.put(
        f"/solicitacoes/{solicitacao_id}", json=update, headers=headers
    )
    assert response_update.status_code == 200
    assert response_update.json()["descricao"] == "Item atualizado"
    assert response_update.json()["status"] == "aprovado"


def test_deletar_solicitacao(usuario_autenticado):
    _, headers = usuario_autenticado
    response = client.post(
        "/solicitacoes/", json={"descricao": "Item para deletar"}, headers=headers
    )
    solicitacao_id = response.json()["id"]

    response_delete = client.delete(f"/solicitacoes/{solicitacao_id}", headers=headers)
    assert response_delete.status_code == 204
