import random
from unittest.mock import patch

import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


# Gera um usuário de teste com código aleatório
@pytest.fixture
def usuario_teste_unico():
    codigo = random.randint(100000, 999999)
    return {
        "codigo_funcionario": codigo,
        "nome": "Usuário Teste",
        "email": f"{codigo}@empresa.com",
        "senha": "senhaSegura123",
    }


# Teste de criação de usuário com funcionário existente (mockado)
@patch("app.services.usuario_service.verificar_funcionario_firebird")
def test_criar_usuario(mock_verificar_funcionario, usuario_teste_unico):
    mock_verificar_funcionario.return_value = {
        "CDFUN": usuario_teste_unico["codigo_funcionario"]
    }

    response = client.post("/usuarios", json=usuario_teste_unico)

    assert response.status_code == 201
    data = response.json()
    assert data["codigo_funcionario"] == usuario_teste_unico["codigo_funcionario"]
    assert data["nome"] == usuario_teste_unico["nome"]


# Teste de login com credenciais válidas
@patch("app.services.usuario_service.verificar_funcionario_firebird")
def test_login_usuario(mock_verificar_funcionario, usuario_teste_unico):
    mock_verificar_funcionario.return_value = {
        "CDFUN": usuario_teste_unico["codigo_funcionario"]
    }

    # Primeiro cria o usuário
    client.post("/usuarios", json=usuario_teste_unico)

    # Faz login com os dados criados
    payload = {
        "codigo_funcionario": usuario_teste_unico["codigo_funcionario"],
        "senha": usuario_teste_unico["senha"],
    }

    response = client.post("/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
