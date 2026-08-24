import pytest
from fastapi.testclient import TestClient
from asep.main import app  # Corrected import statement to reflect the correct module path
from db.models import User, Transaction, Budget
from sqlalchemy.orm import Session
from db.database import get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    # Setup code for creating a new database session
    pass

def test_signup(db_session):
    response = client.post("/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "username": "testuser"}

def test_login_success(db_session):
    client.post("/signup", json={"username": "testuser", "password": "testpass"})
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful", "username": "testuser"}

def test_login_failure(db_session):
    response = client.post("/login", json={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}

def test_create_transaction(db_session):
    response = client.post("/transactions", json={"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"})
    assert response.status_code == 200
    assert response.json()["amount"] == 1000
    assert response.json()["category"] == "Food"

def test_update_transaction(db_session):
    create_response = client.post("/transactions", json={"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"})
    transaction_id = create_response.json()["id"]
    update_response = client.put(f"/transactions/{transaction_id}", json={"amount": 1500})
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 1500

def test_delete_transaction(db_session):
    create_response = client.post("/transactions", json={"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"})
    transaction_id = create_response.json()["id"]
    delete_response = client.delete(f"/transactions/{transaction_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Transaction deleted successfully"}

def test_get_transactions(db_session):
    client.post("/transactions", json={"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"})
    response = client.get("/transactions")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_filtered_transactions(db_session):
    client.post("/transactions", json={"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"})
    response = client.get("/transactions/filter?category=Food")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_budget(db_session):
    response = client.post("/budgets/", json={"category": "Food", "monthly_budget": 5000})
    assert response.status_code == 200
    assert response.json()["category"] == "Food"

def test_update_budget(db_session):
    client.post("/budgets/", json={"category": "Food", "monthly_budget": 5000})
    response = client.put("/budgets/Food", json={"monthly_budget": 6000})
    assert response.status_code == 200
    assert response.json()["monthly_budget"] == 6000

def test_get_budget(db_session):
    client.post("/budgets/", json={"category": "Food", "monthly_budget": 5000})
    response = client.get("/budgets/Food")
    assert response.status_code == 200
    assert response.json()["category"] == "Food"
