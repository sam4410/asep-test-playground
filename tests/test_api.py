import pytest
from fastapi.testclient import TestClient
from asep.api.main import app
from asep.db.models import Note
from sqlalchemy.orm import Session
from asep.db.database import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    db: Session = SessionLocal()
    yield db
    db.close()

def test_create_note_success(db_session):
    response = client.post("/api/v1/notes", json={"title": "Test Note", "body": "This is a test note."})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Note"
    assert data["body"] == "This is a test note."
    assert "created_at" in data

def test_create_note_missing_title(db_session):
    response = client.post("/api/v1/notes", json={"body": "This note has no title."})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_note_missing_body(db_session):
    response = client.post("/api/v1/notes", json={"title": "No Body Note"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_note_empty_fields(db_session):
    response = client.post("/api/v1/notes", json={"title": "", "body": ""})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_note_invalid_data(db_session):
    response = client.post("/api/v1/notes", json={"title": 123, "body": 456})
    assert response.status_code == 422  # Unprocessable Entity

def test_static_directory_exists():
    import os
    assert os.path.exists("static"), "Static directory does not exist."
