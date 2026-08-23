import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
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

def test_create_product(setup_database):
    response = client.post("/api/v1/products", json={
        "name": "Integration Test Product",
        "description": "A product for integration testing",
        "price": 15.99,
        "stock_quantity": 50
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Integration Test Product"

def test_get_product(setup_database):
    response = client.post("/api/v1/products", json={
        "name": "Integration Test Product",
        "description": "A product for integration testing",
        "price": 15.99,
        "stock_quantity": 50
    })
    product_id = response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

def test_update_product(setup_database):
    response = client.post("/api/v1/products", json={
        "name": "Integration Test Product",
        "description": "A product for integration testing",
        "price": 15.99,
        "stock_quantity": 50
    })
    product_id = response.json()["id"]

    updated_data = {
        "name": "Updated Integration Test Product",
        "description": "An updated product for integration testing",
        "price": 17.99,
        "stock_quantity": 30
    }
    response = client.put(f"/api/v1/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]

def test_delete_product(setup_database):
    response = client.post("/api/v1/products", json={
        "name": "Integration Test Product",
        "description": "A product for integration testing",
        "price": 15.99,
        "stock_quantity": 50
    })
    product_id = response.json()["id"]

    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 404

def test_get_nonexistent_product(setup_database):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"