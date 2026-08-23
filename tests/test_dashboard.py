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

client = TestClient(app)

@pytest.fixture
def db_session():
    # Setup code for creating a new database session
    # This should be replaced with actual session creation logic
    pass

def test_get_dashboard(db_session):
    # Assuming a user with ID 1 exists and has expenses
    response = client.get("/dashboard?user_id=1")
    assert response.status_code == 200
    assert "total_spent" in response.json()
    assert "category_breakdown" in response.json()

def test_get_dashboard_no_expenses(db_session):
    # Assuming a user with ID 2 exists and has no expenses
    response = client.get("/dashboard?user_id=2")
    assert response.status_code == 200
    assert response.json()["total_spent"] == 0
    assert response.json()["category_breakdown"] == {}

def test_get_dashboard_invalid_user(db_session):
    # Test with an invalid user ID
    response = client.get("/dashboard?user_id=999")  # Assuming this ID does not exist
    assert response.status_code == 404  # Assuming the endpoint handles this case
    assert "detail" in response.json()

def test_get_dashboard_with_expenses(db_session):
    # Assuming a user with ID 1 exists and has expenses
    # Create some test expenses for the user
    client.post("/expenses", json={
        "amount": 1000,
        "category": "Food",
        "date": "2023-10-01",
        "user_id": 1
    })
    client.post("/expenses", json={
        "amount": 500,
        "category": "Transport",
        "date": "2023-10-02",
        "user_id": 1
    })

    response = client.get("/dashboard?user_id=1")
    assert response.status_code == 200
    assert response.json()["total_spent"] == 1500
    assert response.json()["category_breakdown"]["Food"] == 1000
    assert response.json()["category_breakdown"]["Transport"] == 500
