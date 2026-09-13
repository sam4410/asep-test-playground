from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_predefined_habits_include_daily_water_habit(client):
    response = client.get("/api/habits/predefined")

    assert response.status_code == 200
    habits = response.json()
    water_habit = next(
        habit
        for habit in habits
        if habit["id"] == "drink-6-liters-of-water"
    )

    assert water_habit == {
        "id": "drink-6-liters-of-water",
        "name": "Drink 6 Liters of Water",
        "description": "Drink 6 liters of water per day.",
        "weekdays": [0, 1, 2, 3, 4, 5, 6],
        "template_key": "drink-6-liters-of-water",
        "predefined": True,
    }


def test_stateless_habit_crud_payloads_and_validation(client):
    create_response = client.post(
        "/api/habits",
        json={
            "name": "Read a book",
            "description": "Read for twenty minutes.",
            "weekdays": [0, 2, 4],
            "template_key": "custom-reading",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Read a book"
    assert created["description"] == "Read for twenty minutes."
    assert created["weekdays"] == [0, 2, 4]
    assert created["template_key"] == "custom-reading"
    assert created["predefined"] is False
    assert created["id"]

    habit_id = created["id"]
    update_response = client.put(
        f"/api/habits/{habit_id}",
        json={"name": "Read for twenty minutes", "weekdays": [1, 3, 5]},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == habit_id
    assert updated["name"] == "Read for twenty minutes"
    assert updated["weekdays"] == [1, 3, 5]

    assert client.put(f"/api/habits/{habit_id}", json={}).status_code == 400
    assert (
        client.put(
            f"/api/habits/{habit_id}",
            json={"description": "Name is intentionally omitted."},
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/habits",
            json={"name": "Invalid schedule", "weekdays": [7]},
        ).status_code
        == 422
    )

    delete_response = client.delete(f"/api/habits/{habit_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_completion_accepts_only_completion_for_today(client):
    today = date.today()
    response = client.post(
        "/api/habits/drink-6-liters-of-water/completion",
        json={
            "local_today": today.isoformat(),
            "completion_date": today.isoformat(),
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "habit_id": "drink-6-liters-of-water",
        "completion_date": today.isoformat(),
        "completed": True,
    }

    past_response = client.post(
        "/api/habits/drink-6-liters-of-water/completion",
        json={
            "local_today": today.isoformat(),
            "completion_date": (today - timedelta(days=1)).isoformat(),
            "completed": True,
        },
    )
    assert past_response.status_code == 422


def test_streak_response_contains_current_and_longest_streaks(client):
    through = date.today()
    completed_dates = [
        through - timedelta(days=2),
        through - timedelta(days=1),
        through,
    ]

    response = client.post(
        "/api/habits/drink-6-liters-of-water/streak",
        json={
            "completed_dates": [item.isoformat() for item in completed_dates],
            "weekdays": [0, 1, 2, 3, 4, 5, 6],
            "through": through.isoformat(),
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "current_streak": 3,
        "longest_streak": 3,
    }


def test_streak_response_reports_zero_for_no_completions(client):
    response = client.post(
        "/api/habits/custom/streak",
        json={
            "completed_dates": [],
            "weekdays": [0, 2, 4],
            "through": date.today().isoformat(),
        },
    )

    assert response.status_code == 200
    assert response.json() == {"current_streak": 0, "longest_streak": 0}
