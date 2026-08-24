from asep.api.auth import router as auth_router  # Ensure correct import path
import pytest
from fastapi.testclient import TestClient

from asep.api.auth import router as auth_router  # Ensure correct import path
from fastapi.testclient import TestClient
from asep.api.main import app
from asep.api.auth import router as auth_router  # Ensure correct import path
from asep.db.models import UserModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
