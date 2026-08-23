import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api.main import app
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
