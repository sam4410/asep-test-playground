import sys
import pytest
from api.dashboard import router as include_router  # Ensure correct import path
from fastapi.testclient import TestClient
from asep.api.main import app
from asep.db.models import HabitModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from asep.db.database import Base, get_db

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../asep')))

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

def test_log_habit():
    response = client.post("/api/habits/log", json={
        "user_id": "test_user",
        "habit_name": "Exercise",
        "log_date": "2023-10-01T00:00:00Z"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["habit_name"] == "Exercise"
    assert data["log_date"] == "2023-10-01T00:00:00Z"

def test_log_habit_without_date():
    response = client.post("/api/habits/log", json={
        "user_id": "test_user",
        "habit_name": "Reading"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["habit_name"] == "Reading"
    assert datetime.fromisoformat(data["log_date"][:-1]) <= datetime.utcnow()

def test_log_habit_invalid_user():
    response = client.post("/api/habits/log", json={
        "user_id": "",
        "habit_name": "Cooking"
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_get_habits():
    client.post("/api/habits/log", json={
        "user_id": "test_user",
        "habit_name": "Exercise"
    })
    response = client.get("/api/habits/?user_id=test_user")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) > 0
    assert habits[0]["habit_name"] == "Exercise"

def test_get_habits_not_found():
    response = client.get("/api/habits/?user_id=non_existent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "No habits found for this user"

def test_get_habits_multiple_entries():
    client.post("/api/habits/log", json={
        "user_id": "test_user",
        "habit_name": "Exercise"
    })
    client.post("/api/habits/log", json={
        "user_id": "test_user",
        "habit_name": "Reading"
    })
    response = client.get("/api/habits/?user_id=test_user")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) == 2
    assert any(habit["habit_name"] == "Exercise" for habit in habits)
    assert any(habit["habit_name"] == "Reading" for habit in habits)

