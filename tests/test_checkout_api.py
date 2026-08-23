from api.db import db  # Adjusted import to use the correct path

# Your test code here
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_project_name.database import get_db, Base

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

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_checkout_success(setup_database):
    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 100
    }
    response = client.post("/api/v1/products", json=product_data)
    product_id = response.json()["id"]

    checkout_data = {
        "items": [
            {"product_id": product_id, "quantity": 2}
        ]
    }
    response = client.post("/api/v1/checkout", json=checkout_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Checkout successful"
    assert response.json()["total"] == 21.98  # 10.99 * 2

def test_checkout_insufficient_stock(setup_database):
    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 1
    }
    response = client.post("/api/v1/products", json=product_data)
    product_id = response.json()["id"]

    checkout_data = {
        "items": [
            {"product_id": product_id, "quantity": 2}  # Requesting more than available
        ]
    }
    response = client.post("/api/v1/checkout", json=checkout_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock for product Test Product"

def test_checkout_product_not_found(setup_database):
    checkout_data = {
        "items": [
            {"product_id": 999, "quantity": 1}  # Non-existent product
        ]
    }
    response = client.post("/api/v1/checkout", json=checkout_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found"

def test_checkout_empty_cart(setup_database):
    checkout_data = {
        "items": []  # Empty cart
    }
    response = client.post("/api/v1/checkout", json=checkout_data)
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()  # Check for validation error message
