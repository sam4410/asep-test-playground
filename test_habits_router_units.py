import os
import sys
from datetime import date, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, get_db  # noqa: E402
import models  # noqa: E402
from routers import habits as habits_router  # noqa: E402
from routers import auth as auth_router  # noqa: E402


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.dependency_overrides[get_db] = override_get_db
    app.include_router(auth_router.router)
    app.include_router(habits_router.router)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


def _signup_and_login(client, email="unituser@example.com", password="password123"):
    signup_payload = {"email": email, "password": password}
    resp = client.post("/auth/signup", json=signup_payload)
    assert resp.status_code in (200, 201), resp.text

    login_resp = client.post("/auth/login", json=signup_payload)
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_habit_requires_auth(client):
    resp = client.post(
        "/habits",
        json={"name": "Drink Water", "target_frequency": 7},
    )
    assert resp.status_code in (401, 403)


def test_create_habit_success(client):
    headers = _signup_and_login(client)
    resp = client.post(
        "/habits",
        json={"name": "Drink Water", "target_frequency": 7},
        headers=headers,
    )
    assert resp.status_code in (200, 201), resp.text
    data = resp.json()
    assert data["name"] == "Drink Water"
    assert data["target_frequency"] == 7
    assert "id" in data


def test_list_habits_scoped_to_user(client):
    headers_a = _signup_and_login(client, email="usera@example.com")
    headers_b = _signup_and_login(client, email="userb@example.com")

    client.post(
        "/habits",
        json={"name": "Read Books", "target_frequency": 5},
        headers=headers_a,
    )
    client.post(
        "/habits",
        json={"name": "Meditate", "target_frequency": 7},
        headers=headers_b,
    )

    resp_a = client.get("/habits", headers=headers_a)
    assert resp_a.status_code == 200
    names_a = [h["name"] for h in resp_a.json()]
    assert names_a == ["Read Books"]

    resp_b = client.get("/habits", headers=headers_b)
    assert resp_b.status_code == 200
    names_b = [h["name"] for h in resp_b.json()]
    assert names_b == ["Meditate"]


def test_get_single_habit_not_found(client):
    headers = _signup_and_login(client)
    resp = client.get("/habits/99999", headers=headers)
    assert resp.status_code == 404


def test_update_habit(client):
    headers = _signup_and_login(client)
    create_resp = client.post(
        "/habits",
        json={"name": "Exercise", "target_frequency": 3},
        headers=headers,
    )
    habit_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/habits/{habit_id}",
        json={"name": "Exercise Daily", "target_frequency": 7},
        headers=headers,
    )
    assert update_resp.status_code == 200, update_resp.text
    data = update_resp.json()
    assert data["name"] == "Exercise Daily"
    assert data["target_frequency"] == 7


def test_delete_habit(client):
    headers = _signup_and_login(client)
    create_resp = client.post(
        "/habits",
        json={"name": "Journal", "target_frequency": 1},
        headers=headers,
    )
    habit_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/habits/{habit_id}", headers=headers)
    assert delete_resp.status_code in (200, 204)

    get_resp = client.get(f"/habits/{habit_id}", headers=headers)
    assert get_resp.status_code == 404


def test_checkoff_habit_and_streak(client):
    headers = _signup_and_login(client)
    create_resp = client.post(
        "/habits",
        json={"name": "Stretch", "target_frequency": 7},
        headers=headers,
    )
    habit_id = create_resp.json()["id"]

    checkoff_resp = client.post(f"/habits/{habit_id}/checkoff", headers=headers)
    assert checkoff_resp.status_code in (200, 201), checkoff_resp.text

    detail_resp = client.get(f"/habits/{habit_id}", headers=headers)
    assert detail_resp.status_code == 200
    data = detail_resp.json()
    assert data.get("current_streak", 0) >= 1


def test_cannot_access_other_users_habit(client):
    headers_a = _signup_and_login(client, email="ownera@example.com")
    headers_b = _signup_and_login(client, email="ownerb@example.com")

    create_resp = client.post(
        "/habits",
        json={"name": "Private Habit", "target_frequency": 2},
        headers=headers_a,
    )
    habit_id = create_resp.json()["id"]

    resp = client.get(f"/habits/{habit_id}", headers=headers_b)
    assert resp.status_code == 404