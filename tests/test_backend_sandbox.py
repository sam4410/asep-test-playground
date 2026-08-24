import os
import sys
import pytest
from fastapi.testclient import TestClient
from asep.api.main import app  # Adjusted import statement to reflect the correct module path
from asep.db.models import User, Habit, CheckIn  # Ensure models are imported
# Ensure the static directory exists for testing
if not os.path.exists("static"):
    os.makedirs("static")
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
@pytest.fixture
def create_user(client):
    response = client.post("/signup", json={
        "username": "testuser",
        "password": "password123"
    })
    return response.json()["id"]
def test_create_habit(client, create_user):
    response = client.post("/habits", json={
        "name": "Exercise",
        "target_frequency": "daily"
    }, headers={"Authorization": f"Bearer {create_user}"})  # Assuming token-based auth
    assert response.status_code == 200
    assert response.json()["name"] == "Exercise"
    assert response.json()["target_frequency"] == "daily"
def test_check_in_habit(client, create_user):
    # First create a habit
    habit_response = client.post("/habits", json={
        "name": "Reading",
        "target_frequency": "daily"
    }, headers={"Authorization": f"Bearer {create_user}"})
    habit_id = habit_response.json()["id"]
    # Now check in for the habit
    check_in_response = client.post(f"/habits/{habit_id}/checkin", headers={"Authorization": f"Bearer {create_user}"})
    assert check_in_response.status_code == 200
    assert check_in_response.json()["habit_id"] == habit_id
def test_weekly_progress(client, create_user):
    # Create a habit
    habit_response = client.post("/habits", json={
        "name": "Meditation",
        "target_frequency": "daily"
    }, headers={"Authorization": f"Bearer {create_user}"})
    habit_id = habit_response.json()["id"]
    # Check in for the habit multiple times
    for _ in range(3):
        client.post(f"/habits/{habit_id}/checkin", headers={"Authorization": f"Bearer {create_user}"})
    # Get weekly progress
    progress_response = client.get(f"/habits/{habit_id}/weekly_progress", headers={"Authorization": f"Bearer {create_user}"})
    assert progress_response.status_code == 200
    assert len(progress_response.json()) > 0
    assert progress_response.json()[0]["habit_name"] == "Meditation"
    assert progress_response.json()[0]["completion_count"] == 3
import sys
import os
from fastapi.testclient import TestClient
from asep.api.main import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../asep')))
client = TestClient(app)
from src.api.expenses import router  # Corrected import statement to reflect the correct module path
client = TestClient(router)

 # Add your test cases here
from api.dashboard import include_router
from db.database import get_db, Base, engine
from sqlalchemy.orm import Session
# Create the FastAPI app and include the router
app = FastAPI()
include_router(app)
# Create the database tables
Base.metadata.create_all(bind=engine)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../asep')))
from asep.api.expenses import router
from asep.db.models import Expense  # Ensure this import is correct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from asep.db.database import Base, get_db
from fastapi import FastAPI
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_expense(setup_database):
    response = client.post("/expenses/", json={"amount": 50, "category": "Food", "date": "2023-10-01", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50
    assert data["category"] == "Food"
    assert data["date"] == "2023-10-01"
    assert data["user_id"] == 1

def test_create_expense_invalid_data(setup_database):
    response = client.post("/expenses/", json={"amount": "invalid", "category": "Food", "date": "2023-10-01", "user_id": 1})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_expenses_by_category(setup_database):
    client.post("/expenses/", json={"amount": 50, "category": "Food", "date": "2023-10-01", "user_id": 1})
    client.post("/expenses/", json={"amount": 30, "category": "Food", "date": "2023-10-02", "user_id": 1})
    client.post("/expenses/", json={"amount": 20, "category": "Transport", "date": "2023-10-03", "user_id": 1})

    response = client.get("/expenses/?category=Food")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(expense["category"] == "Food" for expense in data)

def test_get_expenses_by_category_no_expenses(setup_database):
    response = client.get("/expenses/?category=NonExistentCategory")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert data == []  # Expecting an empty list for no expenses
    assert data["user_id"] == 1

def test_create_expense_invalid_data(setup_database):
    response = client.post("/expenses/", json={"amount": "invalid", "category": "Food", "date": "2023-10-01", "user_id": 1})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_expenses_by_category(setup_database):
    client.post("/expenses/", json={"amount": 50.0, "category": "Food", "date": "2023-10-01", "user_id": 1})
    client.post("/expenses/", json={"amount": 30.0, "category": "Food", "date": "2023-10-02", "user_id": 1})
    client.post("/expenses/", json={"amount": 20.0, "category": "Transport", "date": "2023-10-03", "user_id": 1})

    response = client.get("/expenses/?category=Food")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(expense["category"] == "Food" for expense in data)

def test_get_expenses_by_category_no_expenses(setup_database):
    response = client.get("/expenses/?category=NonExistentCategory")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert data == []  # Expecting an empty list for no expenses