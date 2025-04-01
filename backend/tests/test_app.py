import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_returns_status_200():
    response = client.get("/")
    assert response.status_code == 200
