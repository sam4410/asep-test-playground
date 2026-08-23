from ..api.main import app  # Adjusted import to use relative path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.models import Base, User, Task

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

def test_create_task(client):
    # Create a user to assign the task to
    user = User(username="testuser", password="testpass")
    db = next(client.dependency_overrides[get_db]())
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": user.id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task."
    assert data["status"] == "todo"

def test_create_task_missing_title(client):
    response = client.post("/api/v1/tasks", json={
        "description": "This is a test task.",
        "assignee_id": 1
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_create_task_invalid_assignee(client):
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": 999  # Invalid assignee_id
    })
    assert response.status_code == 404  # Not Found

def test_get_task(client):
    # Create a user to assign the task to
    user = User(username="testuser", password="testpass")
    db = next(client.dependency_overrides[get_db]())
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a task
    task_response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": user.id
    })
    task_id = task_response.json()["id"]

    # Get the task
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"

def test_get_task_not_found(client):
    response = client.get("/api/v1/tasks/999")  # Non-existent task ID
    assert response.status_code == 404  # Not Found

def test_update_task(client):
    # Create a user to assign the task to
    user = User(username="testuser", password="testpass")
    db = next(client.dependency_overrides[get_db]())
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a task
    task_response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": user.id
    })
    task_id = task_response.json()["id"]

    # Update the task
    response = client.put(f"/api/v1/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "This is an updated test task.",
        "assignee_id": user.id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"

def test_delete_task(client):
    # Create a user to assign the task to
    user = User(username="testuser", password="testpass")
    db = next(client.dependency_overrides[get_db]())
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a task
    task_response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": user.id
    })
    task_id = task_response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted successfully"}

def test_delete_task_not_found(client):
    response = client.delete("/api/v1/tasks/999")  # Non-existent task ID
    assert response.status_code == 404  # Not Found
sys.path.append(str(Path(__file__).resolve().parent.parent))


sys.path.append(str(Path(__file__).resolve().parent.parent))

from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

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
def test_create_category(client):
    response = client.post("/categories", json={
        "name": "Groceries",
        "user_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Groceries"
    assert data["user_id"] == 1

def test_create_category_invalid_data(client):
    response = client.post("/categories", json={
        "name": "",  # Invalid name
        "user_id": 1
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_get_categories(client):
    client.post("/categories", json={
        "name": "Groceries",
        "user_id": 1
    })
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Groceries"

def test_get_categories_empty(client):
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0