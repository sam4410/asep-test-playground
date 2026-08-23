from api.db import db  # Adjusted import to use the correct path

# Your test code here
from sqlalchemy.orm import sessionmaker
from database import get_db, Base

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

def test_create_product(setup_database):
    response = client.post("/api/v1/products", json={
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 100
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_get_product(setup_database):
    client.post("/api/v1/products", json={
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 100
    })
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_nonexistent_product(setup_database):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_update_product(setup_database):
    client.post("/api/v1/products", json={
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 100
    })
    response = client.put("/api/v1/products/1", json={
        "name": "Updated Product",
        "description": "An updated product for testing",
        "price": 12.99,
        "stock_quantity": 80
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_delete_product(setup_database):
    client.post("/api/v1/products", json={
        "name": "Test Product",
        "description": "A product for testing",
        "price": 10.99,
        "stock_quantity": 100
    })
    response = client.delete("/api/v1/products/1")
    assert response.status_code == 204

def test_delete_nonexistent_product(setup_database):
    response = client.delete("/api/v1/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"