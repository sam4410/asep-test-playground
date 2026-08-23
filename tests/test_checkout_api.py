from ..api.main import app  # Adjusted import to use relative path
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
