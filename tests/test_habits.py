import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db  # Ensure this line is correct
client = TestClient(app)
def test_log_habit():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Habit"
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
def test_get_habit_streak():
    # First, log a habit to ensure it exists
    client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    
    # Now, retrieve the streak for the habit (assuming habit_id is 1)
    response = client.get("/habits/streak/1")
    assert response.status_code == 200
    assert "streak_count" in response.json()
    assert response.json()["streak_count"] == 0  # Default streak count should be 0
def test_get_habit_streak_not_found():
    response = client.get("/habits/streak/999")  # Assuming habit_id 999 does not exist
    assert response.status_code == 404  # Not Found for non-existent habit
    assert response.json() == {"detail": "Habit not found"}
from api.habits import app
from fastapi.testclient import TestClient
from db.models import Habit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db  # Ensure this line is correct
client = TestClient(app)

def test_log_habit():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Habit"

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
