from main import app  # Adjusted import to match the correct module structure
from fastapi.testclient import TestClient
from main import app
from db.models import Expense
from database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@pytest.fixture(scope="module")
def test_db():
    # Setup the test database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    # Teardown the test database
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c

def test_create_expense(client):
    response = client.post("/expenses", json={
        "amount": 50.0,
        "category": "Food",
        "date": "2023-10-01",
        "user_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50.0
    assert data["category"] == "Food"
    assert data["date"] == "2023-10-01"
    assert data["user_id"] == 1

def test_create_expense_invalid_data(client):
    response = client.post("/expenses", json={
        "amount": "invalid_amount",  # Invalid amount
        "category": "Food",
        "date": "2023-10-01",
        "user_id": 1
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_get_expenses_by_category(client):
    client.post("/expenses", json={
        "amount": 50.0,
        "category": "Food",
        "date": "2023-10-01",
        "user_id": 1
    })
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["amount"] == 50.0

def test_get_expenses_by_category_not_found(client):
    response = client.get("/expenses?category=NonExistentCategory")
    assert response.status_code == 404  # Not Found
    assert response.json() == {"detail": "No expenses found for this category"}