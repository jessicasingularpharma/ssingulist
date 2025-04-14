import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_status_200():
    response = client.get("/")
    assert response.status_code == 200
