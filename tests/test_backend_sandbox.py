import sys
import os
# Adjust the import to reflect the correct module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../asep')))
from asep.api.expenses import router
# ... rest of the code ...from app.db.models import Expense  # Ensure this import is correctfrom sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_expense(setup_database):
    response = client.post("/expenses/", json={"amount": 50.0, "category": "Food", "date": "2023-10-01", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50.0
    assert data["category"] == "Food"
    assert data["date"] == "2023-10-01"
    assert data["user_id"] == 1

def test_create_expense_invalid_data(setup_database):
    response = client.post("/expenses/", json={"amount": "invalid", "category": "Food", "date": "2023-10-01", "user_id": 1})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_expenses_by_category(setup_database):
    client.post("/expenses/", json={"amount": 50.0, "category": "Food", "date": "2023-10-01", "user_id": 1})
    client.post("/expenses/", json={"amount": 30.0, "category": "Food", "date": "2023-10-02", "user_id": 1})
    client.post("/expenses/", json={"amount": 20.0, "category": "Transport", "date": "2023-10-03", "user_id": 1})

    response = client.get("/expenses/?category=Food")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(expense["category"] == "Food" for expense in data)

def test_get_expenses_by_category_no_expenses(setup_database):
    response = client.get("/expenses/?category=NonExistentCategory")  # Adjusted endpoint to match the correct path
    assert response.status_code == 200
    data = response.json()
    assert data == []  # Expecting an empty list for no expenses