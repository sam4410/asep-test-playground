import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_task(client):
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task."
    assert data["status"] == "todo"

def test_create_task_missing_title(client):
    response = client.post("/api/v1/tasks", json={
        "description": "This is a test task.",
        "assignee_id": 1
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_create_task_invalid_assignee(client):
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": "invalid_id"  # Invalid assignee_id
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_get_tasks(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_tasks_with_filter(client):
    response = client.get("/api/v1/tasks?assignee_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for task in data:
        assert task["assignee_id"] == 1

def test_get_tasks_with_status_filter(client):
    response = client.get("/api/v1/tasks?status=todo")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for task in data:
        assert task["status"] == "todo"