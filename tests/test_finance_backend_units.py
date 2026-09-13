from datetime import date
from uuid import uuid4

import sqlalchemy

if not hasattr(sqlalchemy, "__all__"):
    sqlalchemy.__all__ = [
        name for name in dir(sqlalchemy) if not name.startswith("_")
    ]

import pytest

import routes


def _credentials():
    return {
        "email": f"{uuid4().hex}@example.com",
        "password": "correct horse battery staple",
    }


def _login(client, credentials):
    signup = client.post("/api/auth/signup", json=credentials)
    assert signup.status_code in (200, 201)

    login = client.post("/api/auth/login", json=credentials)
    assert login.status_code == 200
    body = login.json()
    return body.get("access_token") or body["token"]


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_password_hash_verifies_and_rejects_wrong_or_malformed_values():
    password_hash = routes._hash_password("sufficiently-secret")

    assert password_hash.startswith("pbkdf2_sha256$")
    assert routes._verify_password("sufficiently-secret", password_hash)
    assert not routes._verify_password("different-password", password_hash)
    assert not routes._verify_password("sufficiently-secret", "not-a-password-hash")
    assert not routes._verify_password("sufficiently-secret", None)


def test_bearer_token_contains_subject_and_rejects_tampering(monkeypatch):
    from models import User

    user = User(
        id=str(uuid4()),
        email=f"{uuid4().hex}@example.com",
        hashed_password=routes._hash_password("password"),
    )
    fixed_time = 1_700_000_000
    monkeypatch.setattr(routes.time, "time", lambda: fixed_time)

    token = routes._issue_token(user)
    payload = routes._decode_token(token)

    assert payload["sub"] == str(user.id)
    assert payload["iat"] == fixed_time
    assert payload["exp"] == fixed_time + 3600
    assert routes._decode_token(token + "tampered") is None
    assert routes._decode_token("not.a.valid.token") is None


def test_bearer_token_expiry_is_enforced(monkeypatch):
    from models import User

    user = User(
        id=str(uuid4()),
        email=f"{uuid4().hex}@example.com",
        hashed_password=routes._hash_password("password"),
    )
    issued_at = 2_000_000_000
    monkeypatch.setattr(routes.time, "time", lambda: issued_at)
    token = routes._issue_token(user)

    monkeypatch.setattr(routes.time, "time", lambda: issued_at + 3600)

    assert routes._decode_token(token) is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("12", 1200),
        ("12.34", 1234),
        (12.5, 1250),
    ],
)
def test_parse_amount_converts_valid_currency_values(value, expected):
    assert routes._parse_amount(value) == expected


@pytest.mark.parametrize("value", [None, True, 0, -1, "1.999", "not-money"])
def test_parse_amount_rejects_invalid_currency_values(value):
    with pytest.raises(ValueError):
        routes._parse_amount(value)


def test_currency_amount_is_exact_and_keeps_two_decimal_places():
    assert routes._currency_amount(1234) == "12.34"
    assert routes._currency_amount(5) == "0.05"
    assert routes._currency_amount(0) == "0.00"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-02-01", date(2026, 2, 1)),
        (" 2026-12-31 ", date(2026, 12, 31)),
    ],
)
def test_parse_transaction_date_accepts_iso_dates(value, expected):
    assert routes._parse_transaction_date(value) == expected


@pytest.mark.parametrize("value", ["2026-02-30", "", None, 20260101])
def test_parse_transaction_date_rejects_invalid_dates(value):
    with pytest.raises(ValueError):
        routes._parse_transaction_date(value)


def test_dashboard_month_returns_inclusive_month_boundaries():
    assert routes._dashboard_month("2024-02") == (
        date(2024, 2, 1),
        date(2024, 2, 29),
    )
    assert routes._dashboard_month("2024-12") == (
        date(2024, 12, 1),
        date(2024, 12, 31),
    )

    with pytest.raises(ValueError):
        routes._dashboard_month("2024-2")


def test_transaction_listing_filters_by_authenticated_owner(client):
    first_token = _login(client, _credentials())
    second_token = _login(client, _credentials())

    first_transaction = client.post(
        "/api/transactions",
        headers=_auth_headers(first_token),
        json={
            "amount": "10.00",
            "type": "expense",
            "category": "Food",
            "date": "2026-09-01",
        },
    )
    second_transaction = client.post(
        "/api/transactions",
        headers=_auth_headers(second_token),
        json={
            "amount": "99.00",
            "type": "expense",
            "category": "Private",
            "date": "2026-09-02",
        },
    )
    assert first_transaction.status_code == 201
    assert second_transaction.status_code == 201

    response = client.get(
        "/api/transactions",
        headers=_auth_headers(first_token),
    )

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 1
    assert transactions[0]["category"] == "Food"
    assert transactions[0]["id"] != second_transaction.json()["id"]


def test_dashboard_aggregates_selected_month_and_excludes_other_users(client):
    owner_token = _login(client, _credentials())
    other_token = _login(client, _credentials())

    transactions = [
        (
            owner_token,
            {
                "amount": "100.00",
                "type": "income",
                "category": "Salary",
                "date": "2026-09-01",
            },
        ),
        (
            owner_token,
            {
                "amount": "25.50",
                "type": "expense",
                "category": "Food",
                "date": "2026-09-15",
            },
        ),
        (
            owner_token,
            {
                "amount": "7.00",
                "type": "expense",
                "category": "Food",
                "date": "2026-08-31",
            },
        ),
        (
            other_token,
            {
                "amount": "999.00",
                "type": "expense",
                "category": "Other user",
                "date": "2026-09-10",
            },
        ),
    ]

    for token, payload in transactions:
        response = client.post(
            "/api/transactions",
            headers=_auth_headers(token),
            json=payload,
        )
        assert response.status_code == 201

    response = client.get(
        "/api/dashboard/summary?month=2026-09",
        headers=_auth_headers(owner_token),
    )

    assert response.status_code == 200
    summary = response.json()
    assert summary["period"] == {
        "month": "2026-09",
        "start": "2026-09-01",
        "end": "2026-09-30",
        "timezone": "UTC",
    }
    assert summary["total_balance_cents"] == 6750
    assert summary["monthly_income_cents"] == 10000
    assert summary["monthly_spending_cents"] == 2550
    assert summary["category_spending"] == [
        {
            "category": "Food",
            "amount": "25.50",
            "amount_cents": 2550,
            "formatted_amount": "$25.50",
            "percentage": "100.00",
        }
    ]
    assert all(
        item["category"] != "Other user"
        for item in summary["recent_transactions"]
    )