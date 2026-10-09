import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

import database
from database import Base, SessionLocal, get_db
from main import app
from models import Todo


@pytest.fixture()
def client():
    database_url = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not database_url or not database_url.startswith("postgresql"):
        pytest.skip("TEST_DATABASE_URL or DATABASE_URL must point to PostgreSQL")

    try:
        Base.metadata.create_all(bind=database.engine)
    except SQLAlchemyError as exc:
        pytest.skip(f"PostgreSQL test database is unavailable: {exc}")

    with SessionLocal() as session:
        session.query(Todo).delete()
        session.commit()

    def override_get_db():
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

    with SessionLocal() as session:
        session.query(Todo).delete()
        session.commit()


def test_todo_lifecycle_and_validation(client):
    empty_response = client.get("/api/v1/todos")
    assert empty_response.status_code == 200
    assert empty_response.json() == []

    blank_response = client.post("/api/v1/todos", json={"title": "   "})
    assert blank_response.status_code == 422

    missing_title_response = client.post("/api/v1/todos", json={})
    assert missing_title_response.status_code == 422

    long_title_response = client.post("/api/v1/todos", json={"title": "x" * 501})
    assert long_title_response.status_code == 422

    created_response = client.post(
        "/api/v1/todos",
        json={"title": "Write integration tests"},
    )
    assert created_response.status_code == 201
    created = created_response.json()
    assert created["title"] == "Write integration tests"
    assert created["completed"] is False
    assert isinstance(created["id"], int)
    assert created["created_at"]
    assert created["updated_at"]

    todo_id = created["id"]
    listed_response = client.get("/api/v1/todos")
    assert listed_response.status_code == 200
    assert listed_response.json() == [created]

    completed_response = client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"completed": True},
    )
    assert completed_response.status_code == 200
    assert completed_response.json()["id"] == todo_id
    assert completed_response.json()["completed"] is True

    incomplete_response = client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"completed": False},
    )
    assert incomplete_response.status_code == 200
    assert incomplete_response.json()["completed"] is False

    invalid_update_response = client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"completed": "not-a-boolean"},
    )
    assert invalid_update_response.status_code == 422

    missing_update_response = client.patch(
        "/api/v1/todos/999999999",
        json={"completed": True},
    )
    assert missing_update_response.status_code == 404
    assert missing_update_response.json()["detail"]

    delete_response = client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_delete_response = client.delete(f"/api/v1/todos/{todo_id}")
    assert missing_delete_response.status_code == 404
    assert missing_delete_response.json()["detail"]

    final_response = client.get("/api/v1/todos")
    assert final_response.status_code == 200
    assert final_response.json() == []
