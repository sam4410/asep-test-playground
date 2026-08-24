from asep.api.main import app  # Adjusted import statement to reflect the correct module path
import pytest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from asep.db.models import Product, ShoppingCart, CartItem, OrderHistory
from sqlalchemy.orm import Session
from asep.database import get_db  # Adjusted import statement to reflect the correct module path
import os  # Added import for os

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

def test_static_directory_exists():
    assert os.path.exists("static"), "Static directory does not exist" 
import pytest
from fastapi.testclient import TestClient
from asep.api.main import app  # Adjusted import statement to reflect the correct module path
import os  # Added import for os module
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
client = TestClient(app)

