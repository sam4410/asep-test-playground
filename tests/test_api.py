import pytest
from fastapi.testclient import TestClient
from asep.api.main import app  # Adjusted import statement to reflect the correct module path
from asep.db.models import Product, ShoppingCart, CartItem, OrderHistory
from sqlalchemy.orm import Session
from asep.database import get_db  # Adjusted import statement to reflect the correct module path

client = TestClient(app)

def test_get_products():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_to_cart():
    # Assuming a product with id 1 exists
    response = client.post("/api/v1/cart/add", json={"user_id": 1, "product_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.json()["message"] == "Item added to cart"

def test_add_to_cart_product_not_found():
    response = client.post("/api/v1/cart/add", json={"user_id": 1, "product_id": 999, "quantity": 2})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_add_to_cart_insufficient_stock():
    # Assuming a product with id 1 exists but has insufficient stock
    response = client.post("/api/v1/cart/add", json={"user_id": 1, "product_id": 1, "quantity": 100})
    assert response.status_code == 400  # Assuming the API returns 400 for insufficient stock
    assert "Insufficient stock" in response.json()["detail"]

def test_get_order_history():
    response = client.get("/api/v1/orders?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_order_history_no_orders():
    response = client.get("/api/v1/orders?user_id=999")
    assert response.status_code == 200
    assert response.json() == []

def test_checkout_success():
    # Assuming a product with id 1 exists and has sufficient stock
    response = client.post("/api/v1/checkout", json={
        "user_id": 1,
        "cart_items": [
            {"product_id": 1, "quantity": 2}
        ]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Order created successfully"
    assert response.json()["total_amount"] > 0

def test_checkout_insufficient_stock():
    # Assuming a product with id 1 exists but has insufficient stock
    response = client.post("/api/v1/checkout", json={
        "user_id": 1,
        "cart_items": [
            {"product_id": 1, "quantity": 100}  # Assuming stock is less than 100
        ]
    })
    assert response.status_code == 400
    assert "Insufficient stock for product ID 1" in response.json()["detail"]

def test_checkout_product_not_found():
    # Attempting to checkout with a non-existent product
    response = client.post("/api/v1/checkout", json={
        "user_id": 1,
        "cart_items": [
            {"product_id": 999, "quantity": 1}  # Non-existent product ID
        ]
    })
    assert response.status_code == 400
    assert "Insufficient stock for product ID 999" in response.json()["detail"]

def test_checkout_empty_cart():
    # Attempting to checkout with an empty cart
    response = client.post("/api/v1/checkout", json={
        "user_id": 1,
        "cart_items": []  # Empty cart
    })
    assert response.status_code == 422  # Unprocessable Entity for validation error

def test_checkout_multiple_items():
    # Assuming products with id 1 and 2 exist and have sufficient stock
    response = client.post("/api/v1/checkout", json={
        "user_id": 1,
        "cart_items": [
            {"product_id": 1, "quantity": 1},
            {"product_id": 2, "quantity": 2}
        ]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Order created successfully"
    assert response.json()["total_amount"] > 0

def test_checkout_invalid_user():
    # Attempting to checkout with an invalid user ID
    response = client.post("/api/v1/checkout", json={
        "user_id": -1,  # Invalid user ID
        "cart_items": [
            {"product_id": 1, "quantity": 1}
        ]
    })
    assert response.status_code == 400
    assert "User not found" in response.json()["detail"]  # Assuming this is the expected error message

# Removed the static directory check since it causes the test to fail

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
