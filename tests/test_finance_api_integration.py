import pytest
from uuid import uuid4


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from main import app

    with TestClient(app) as value:
        yield value


def account():
    return {"email": f"{uuid4().hex}@example.com", "password": "correct horse battery staple"}


def headers(token):
    return {"Authorization": f"Bearer {token}"}


def signup_and_login(client, user=None):
    user = user or account()
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201
    assert response.json()["user"]["email"] == user["email"].lower()
    response = client.post("/api/auth/login", json=user)
    assert response.status_code == 200
    return response.json()["token"], user


def transaction(**changes):
    value = {
        "amount": "25.50",
        "type": "expense",
        "category": "Food",
        "date": "2026-09-15",
        "note": "Lunch",
    }
    value.update(changes)
    return value


def test_signup_duplicate_and_login_errors(client):
    user = account()
    created = client.post("/api/auth/signup", json=user)
    assert created.status_code == 201
    assert created.json()["token"]
    duplicate = client.post("/api/auth/signup", json={**user, "email": user["email"].upper()})
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]
    assert client.post("/api/auth/login", json={**user, "password": "wrong"}).status_code == 401
    unknown = {"email": f"{uuid4().hex}@example.com", "password": user["password"]}
    assert client.post("/api/auth/login", json=unknown).status_code == 401
    login = client.post("/api/auth/login", json=user)
    assert login.status_code == 200
    assert login.json()["user"]["id"] == created.json()["user"]["id"]


def test_bearer_authentication_and_logout(client):
    token, user = signup_and_login(client)
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers=headers("invalid")).status_code == 401
    me = client.get("/api/auth/me", headers=headers(token))
    assert me.status_code == 200
    assert me.json()["user"]["email"] == user["email"]
    assert client.get("/api/transactions").status_code == 401
    assert client.get("/api/transactions", headers=headers(token)).json() == []
    assert client.post("/api/auth/logout", headers=headers(token)).status_code == 200
    assert client.get("/api/auth/me", headers=headers(token)).status_code == 401


def test_signup_and_transaction_validation_errors(client):
    invalid = [
        {"email": "not-an-email", "password": "long enough password"},
        {"email": f"{uuid4().hex}@example.com", "password": "short"},
        {},
        {"email": "missing-password@example.com"},
    ]
    for payload in invalid:
        response = client.post("/api/auth/signup", json=payload)
        assert response.status_code in (400, 422)
        assert response.json()
    token, _ = signup_and_login(client)
    invalid_transactions = [
        {"type": "expense", "category": "Food", "date": "2026-09-01"},
        transaction(amount="0"),
        transaction(amount="1.999"),
        transaction(type="transfer"),
        transaction(category=""),
        transaction(date="2026-02-30"),
    ]
    for payload in invalid_transactions:
        response = client.post("/api/transactions", headers=headers(token), json=payload)
        assert response.status_code in (400, 422)
        assert response.json()


def test_transaction_crud_and_update_validation(client):
    token, _ = signup_and_login(client)
    auth = headers(token)
    created = client.post("/api/transactions", headers=auth, json=transaction())
    assert created.status_code == 201
    item = created.json()
    endpoint = f"/api/transactions/{item['id']}"
    assert item["amount"] == "25.50"
    assert client.get("/api/transactions", headers=auth).json()[0]["id"] == item["id"]
    updated = client.patch(
        endpoint,
        headers=auth,
        json=transaction(amount="100.00", type="income", category="Salary"),
    )
    assert updated.status_code == 200
    assert updated.json()["amount"] == "100.00"
    assert updated.json()["type"] == "income"
    assert client.patch(endpoint, headers=auth, json={"amount": "not-money"}).status_code in (400, 422)
    assert client.patch(endpoint, headers=auth, json={"unexpected": "value"}).status_code in (400, 422)
    assert client.delete(endpoint, headers=auth).status_code == 200
    assert client.delete(endpoint, headers=auth).status_code == 404


def test_dashboard_totals_categories_and_recent_order(client):
    token, _ = signup_and_login(client)
    auth = headers(token)
    records = [
        transaction(amount="100.00", type="income", category="Salary", date="2026-09-01"),
        transaction(amount="20.00", category="Food", date="2026-09-20"),
        transaction(amount="10.00", category="Utilities", date="2026-09-10"),
        transaction(amount="5.00", category="Food", date="2026-08-31"),
        transaction(amount="7.00", category="Travel", date="2026-09-25"),
    ]
    ids = []
    for record in records:
        response = client.post("/api/transactions", headers=auth, json=record)
        assert response.status_code == 201
        ids.append(response.json()["id"])
    response = client.get("/api/dashboard/summary?month=2026-09", headers=auth)
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_balance_cents"] == 5800
    assert summary["monthly_income_cents"] == 10000
    assert summary["monthly_spending_cents"] == 3700
    assert {row["category"] for row in summary["category_spending"]} == {"Food", "Travel", "Utilities"}
    assert [row["date"] for row in summary["recent_transactions"]] == [
        "2026-09-25", "2026-09-20", "2026-09-10", "2026-09-01", "2026-08-31"
    ]
    assert summary["recent_transactions"][0]["id"] == ids[-1]


def test_user_cannot_read_or_mutate_another_users_transaction(client):
    owner_token, _ = signup_and_login(client)
    other_token, _ = signup_and_login(client)
    created = client.post(
        "/api/transactions", headers=headers(owner_token), json=transaction()
    )
    assert created.status_code == 201
    transaction_id = created.json()["id"]
    other_auth = headers(other_token)
    assert client.get("/api/transactions", headers=other_auth).json() == []
    summary = client.get("/api/dashboard/summary?month=2026-09", headers=other_auth)
    assert summary.status_code == 200
    assert summary.json()["total_balance_cents"] == 0
    assert summary.json()["recent_transactions"] == []
    endpoint = f"/api/transactions/{transaction_id}"
    assert client.get(endpoint, headers=other_auth).status_code == 404
    assert client.patch(endpoint, headers=other_auth, json={"amount": "999.00"}).status_code == 404
    assert client.delete(endpoint, headers=other_auth).status_code == 404
    own = client.get("/api/transactions", headers=headers(owner_token))
    assert own.json()[0]["id"] == transaction_id


def test_dashboard_requires_authentication(client):
    response = client.get("/api/dashboard/summary?month=2026-09")
    assert response.status_code == 401
    response = client.get("/api/dashboard/summary", headers=headers("invalid-token"))
    assert response.status_code == 401


def test_empty_dashboard_for_new_user(client):
    token, _ = signup_and_login(client)
    response = client.get("/api/dashboard/summary?month=2026-09", headers=headers(token))
    assert response.status_code == 200
    body = response.json()
    assert body["total_balance_cents"] == 0
    assert body["monthly_income_cents"] == 0
    assert body["monthly_spending_cents"] == 0
    assert body["category_spending"] == []
    assert body["recent_transactions"] == []


def test_transaction_list_remains_empty_after_rejected_writes(client):
    token, _ = signup_and_login(client)
    auth = headers(token)
    response = client.post("/api/transactions", headers=auth, json=transaction(amount="-1"))
    assert response.status_code in (400, 422)
    assert client.get("/api/transactions", headers=auth).json() == []