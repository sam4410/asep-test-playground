import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../asep/api')))
from asep.api.auth import router as auth_router  # Adjusted import statement to reflect the correct module pathfrom sqlalchemy.orm import Session
from asep.db.models import User

client = TestClient(app)

def test_signup_success():
    response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_signup_username_already_exists():
    # First signup
    client.post("/api/auth/signup", json={
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    })
    # Attempt to signup again with the same username
    response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "password": "newpassword",
        "email": "new@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_success():
    client.post("/api/auth/signup", json={
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    })
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username or password"

def test_login_missing_fields():
    response = client.post("/api/auth/login", json={
        "username": "testuser"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username and password are required"
