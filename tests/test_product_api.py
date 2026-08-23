from api.main import app  # Adjusted import to use absolute path
import pytest
from fastapi.testclient import TestClient
from api.db.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_habit():
    response = client.post("/habits", json={"name": "Test Habit", "target_frequency": 1})
    assert response.status_code == 200
    assert "id" in response.json()
def test_log_habit():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Habit"
def test_get_habit_streak():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    habit_id = response.json()["id"]
    
    response = client.get(f"/habits/streak/{habit_id}")
    assert response.status_code == 200
    assert "streak_count" in response.json()
    assert response.json()["streak_count"] == 0  # Default streak count should be 0
def test_get_habit_streak_not_found():
    response = client.get("/habits/streak/999")  # Assuming habit_id 999 does not exist
    assert response.status_code == 404  # Not Found for non-existent habit
    assert response.json() == {"detail": "Habit not found"}
def test_log_habit_invalid_user():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": -1})
    assert response.status_code == 422  # Unprocessable Entity for invalid input
def test_get_habits():
    response = client.get("/habits?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of habits
def test_get_habits_no_habits():
    response = client.get("/habits?user_id=999")  # Assuming user_id 999 has no habits
    assert response.status_code == 200
    assert response.json() == []  # Should return an empty list
sys.path.append(str(Path(__file__).resolve().parent.parent))


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True

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