from db import models
# Your test code here...
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
    response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task.",
        "assignee_id": 1
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
        "assignee_id": "invalid_id"  # Invalid assignee_id
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_task_status_enum(client):
    task = Task(
        title="Enum Test Task",
        description="Testing enum status.",
        assignee_id=1,
        status=TaskStatus.DONE
    )
    assert task.status == TaskStatus.DONE
    assert task.status != TaskStatus.TODO
    assert task.status != TaskStatus.IN_PROGRESS
