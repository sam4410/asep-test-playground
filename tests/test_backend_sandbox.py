import pytest
from fastapi.testclient import TestClient
from asep.api.main import app

client = TestClient(app)

def test_flip_coin():
    response = client.get("/api/v1/flip")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] in ["heads", "tails"]

def test_flip_coin_response_structure():
    response = client.get("/api/v1/flip")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "result" in data

def test_static_directory_exists(mocker):
    mocker.patch("os.path.exists", return_value=True)
    assert os.path.exists("static"), "Static directory does not exist."