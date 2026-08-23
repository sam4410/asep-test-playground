from ..api.main import app  # Adjusted import to use relative path
from fastapi.testclient import TestClient
from api.db.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

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

def test_create_habit():
    response = client.post("/habits", json={"name": "Test Habit", "target_frequency": 1})
    assert response.status_code == 200
    assert "id" in response.json()
def test_log_habit():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Habit"
def test_get_habit_streak():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    habit_id = response.json()["id"]
    
    response = client.get(f"/habits/streak/{habit_id}")
    assert response.status_code == 200
    assert "streak_count" in response.json()
    assert response.json()["streak_count"] == 0  # Default streak count should be 0
def test_get_habit_streak_not_found():
    response = client.get("/habits/streak/999")  # Assuming habit_id 999 does not exist
    assert response.status_code == 404  # Not Found for non-existent habit
    assert response.json() == {"detail": "Habit not found"}
def test_log_habit_invalid_user():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": -1})
    assert response.status_code == 422  # Unprocessable Entity for invalid input
def test_get_habits():
    response = client.get("/habits?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of habits
def test_get_habits_no_habits():
    response = client.get("/habits?user_id=999")  # Assuming user_id 999 has no habits
    assert response.status_code == 200
    assert response.json() == []  # Should return an empty list
sys.path.append(str(Path(__file__).resolve().parent.parent))


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