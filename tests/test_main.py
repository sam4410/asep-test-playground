import pytest
from fastapi.testclient import TestClient
from main import app  # Updated import to reflect the correct module structure
from database import SessionLocal, engine
from models import Base, User, Habit

@pytest.fixture(scope="module")
def test_client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_user(test_client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = test_client.post("/auth/signup", json=user_data)
    return response.json()["access_token"]

def test_signup(test_client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpassword"
    }
    response = test_client.post("/auth/signup", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login(test_client, create_user):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = test_client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_habit(test_client, create_user):
    habit_data = {
        "name": "Read a book"
    }
    response = test_client.post("/habits/", json=habit_data, headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 200
    assert response.json()["name"] == habit_data["name"]

def test_read_habits(test_client, create_user):
    response = test_client.get("/habits/", headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_habit(test_client, create_user):
    habit_data = {
        "name": "Updated Habit"
    }
    # First create a habit to update
    create_response = test_client.post("/habits/", json={"name": "Habit to Update"}, headers={"Authorization": f"Bearer {create_user}"})
    habit_id = create_response.json()["id"]
    
    response = test_client.put(f"/habits/{habit_id}", json=habit_data, headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 200
    assert response.json()["name"] == habit_data["name"]

def test_delete_habit(test_client, create_user):
    # First create a habit to delete
    create_response = test_client.post("/habits/", json={"name": "Habit to Delete"}, headers={"Authorization": f"Bearer {create_user}"})
    habit_id = create_response.json()["id"]
    
    response = test_client.delete(f"/habits/{habit_id}", headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Habit deleted successfully"}