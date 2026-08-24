from fastapi.testclient import TestClient
from src.api.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import User, Task
from src.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

Base.metadata.create_all(bind=engine)

def test_create_task():
    # First, create a user to assign the task to
    user_response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    })
    assert user_response.status_code == 200

    # Now create a task
    response = client.post("/api/tasks/", json={
        "title": "New Task",
        "description": "Task description",
        "assignee": "testuser",
        "due_date": "2023-12-31",
        "status": "todo"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully"

def test_get_tasks():
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task():
    # Create a task first
    task_response = client.post("/api/tasks/", json={
        "title": "Another Task",
        "description": "Another task description",
        "assignee": "testuser",
        "due_date": "2023-12-31",
        "status": "todo"
    })
    task_id = task_response.json()["task_id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Another Task"
    assert response.json()["description"] == "Another task description"