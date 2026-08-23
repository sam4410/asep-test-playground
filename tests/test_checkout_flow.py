import pytest
from fastapi.testclient import TestClient
from api.main import app
from db.models import Product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from api.dependencies import get_db

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def sample_products(test_db):
    db = test_db
    products = [
        Product(name="Product 1", description="A product", price=10.0, stock_quantity=100, category_id=1),
        Product(name="Product 2", description="Another product", price=20.0, stock_quantity=50, category_id=1)
    ]
    db.add_all(products)
    db.commit()
    return products

def test_checkout_success(client, sample_products):
    cart = {
        "1": 2,
        "2": 1
    }
    response = client.post("/api/v1/checkout", json=cart)
    assert response.status_code == 200
    assert response.json() == {"message": "Checkout successful", "total": 40.0}

def test_checkout_insufficient_stock(client, sample_products):
    cart = {
        "1": 200  # Requesting more than available stock
    }
    response = client.post("/api/v1/checkout", json=cart)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock for product Product 1."

def test_checkout_product_not_found(client, sample_products):
    cart = {
        "999": 1  # Non-existent product ID
    }
    response = client.post("/api/v1/checkout", json=cart)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 999 not found."

def test_checkout_empty_cart(client):
    cart = {}
    response = client.post("/api/v1/checkout", json=cart)
    assert response.status_code == 200
    assert response.json() == {"message": "Checkout successful", "total": 0.0}
