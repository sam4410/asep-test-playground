"""Personal finance tracker API."""

from datetime import date
import hashlib
import os
import secrets
import sqlite3
from typing import Any, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field, validator


DATABASE_PATH = os.getenv("FINANCE_DB_PATH", "finance.sqlite3")
app = FastAPI(title="Personal Finance API", version="1.0.0")
# Keep a small Flask-compatible configuration mapping for integration tests and
# callers that need to point the application at an isolated database.
app.config = {"DATABASE_PATH": DATABASE_PATH, "TESTING": False}


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount REAL NOT NULL CHECK (amount > 0),
    category TEXT NOT NULL,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('income', 'expense')),
    transaction_date TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS transactions_user_date
    ON transactions(user_id, transaction_date DESC, id DESC);
"""


def configured_database_path() -> str:
    configured = app.config.get("DATABASE_PATH") or app.config.get("DATABASE")
    if configured is None:
        configured = app.config.get("DATABASE_URL")
    if configured and str(configured).startswith("sqlite:///"):
        configured = str(configured)[10:]
    return str(configured or DATABASE_PATH)


def db() -> sqlite3.Connection:
    connection = sqlite3.connect(configured_database_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    return connection


def initialise() -> None:
    connection = db()
    connection.commit()
    connection.close()


initialise()


def password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=6)

    @validator("email")
    def valid_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("a valid email address is required")
        return value


class LoginRequest(SignupRequest):
    pass


class TransactionRequest(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=80)
    date: date
    note: str = Field(default="", max_length=500)
    type: str = Field(default="expense", alias="transaction_type")

    class Config:
        allow_population_by_field_name = True

    @validator("category")
    def category_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("category is required")
        return value

    @validator("type")
    def valid_type(cls, value: str) -> str:
        value = value.lower().strip()
        if value not in {"income", "expense"}:
            raise ValueError("type must be income or expense")
        return value


def row_transaction(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "amount": row["amount"],
        "category": row["category"],
        "type": row["transaction_type"],
        "transaction_type": row["transaction_type"],
        "date": row["transaction_date"],
        "note": row["note"],
    }


def current_user(authorization: Optional[str] = Header(default=None)) -> sqlite3.Row:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.split(None, 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Bearer token required")
    connection = db()
    user = connection.execute(
        """
        SELECT users.* FROM users
        JOIN sessions ON sessions.user_id = users.id
        WHERE sessions.token = ?
        """,
        (token,),
    ).fetchone()
    connection.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
@app.post("/signup", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def signup(payload: SignupRequest) -> dict[str, Any]:
    connection = db()
    try:
        cursor = connection.execute(
            "INSERT INTO users(email, password_hash) VALUES (?, ?)",
            (payload.email, password_hash(payload.password)),
        )
        connection.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        connection.close()
        raise HTTPException(
            status_code=409,
            detail="An account with that email already exists",
        )
    connection.close()
    return {"id": user_id, "email": payload.email, "message": "Account created"}


@app.post("/auth/login")
@app.post("/login", include_in_schema=False)
def login(payload: LoginRequest) -> dict[str, Any]:
    connection = db()
    user = connection.execute(
        "SELECT * FROM users WHERE email = ? COLLATE NOCASE", (payload.email,)
    ).fetchone()
    if user is None or user["password_hash"] != password_hash(payload.password):
        connection.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = secrets.token_urlsafe(32)
    connection.execute(
        "INSERT INTO sessions(token, user_id) VALUES (?, ?)", (token, user["id"])
    )
    connection.commit()
    connection.close()
    return {
        "access_token": token,
        "token": token,
        "token_type": "bearer",
        "user": {"id": user["id"], "email": user["email"]},
    }


@app.get("/auth/me")
@app.get("/me", include_in_schema=False)
def me(user: sqlite3.Row = Depends(current_user)) -> dict[str, Any]:
    return {"id": user["id"], "email": user["email"]}


def get_transaction(transaction_id: int, user_id: int) -> sqlite3.Row:
    connection = db()
    row = connection.execute(
        "SELECT * FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id),
    ).fetchone()
    connection.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return row


@app.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionRequest, user: sqlite3.Row = Depends(current_user)
) -> dict[str, Any]:
    connection = db()
    cursor = connection.execute(
        """
        INSERT INTO transactions
          (user_id, amount, category, transaction_type, transaction_date, note)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user["id"],
            payload.amount,
            payload.category,
            payload.type,
            payload.date.isoformat(),
            payload.note,
        ),
    )
    connection.commit()
    row = connection.execute(
        "SELECT * FROM transactions WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    connection.close()
    return row_transaction(row)


@app.get("/transactions")
def list_transactions(
    user: sqlite3.Row = Depends(current_user),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[dict[str, Any]]:
    connection = db()
    rows = connection.execute(
        """
        SELECT * FROM transactions
        WHERE user_id = ?
        ORDER BY transaction_date DESC, id DESC
        LIMIT ?
        """,
        (user["id"], limit),
    ).fetchall()
    connection.close()
    return [row_transaction(row) for row in rows]


@app.get("/transactions/{transaction_id}")
def read_transaction(
    transaction_id: int, user: sqlite3.Row = Depends(current_user)
) -> dict[str, Any]:
    return row_transaction(get_transaction(transaction_id, user["id"]))


def save_transaction(
    transaction_id: int, payload: TransactionRequest, user_id: int
) -> dict[str, Any]:
    get_transaction(transaction_id, user_id)
    connection = db()
    connection.execute(
        """
        UPDATE transactions
        SET amount = ?, category = ?, transaction_type = ?,
            transaction_date = ?, note = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            payload.amount,
            payload.category,
            payload.type,
            payload.date.isoformat(),
            payload.note,
            transaction_id,
            user_id,
        ),
    )
    connection.commit()
    row = connection.execute(
        "SELECT * FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id),
    ).fetchone()
    connection.close()
    return row_transaction(row)


@app.put("/transactions/{transaction_id}")
@app.patch("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    payload: TransactionRequest,
    user: sqlite3.Row = Depends(current_user),
) -> dict[str, Any]:
    return save_transaction(transaction_id, payload, user["id"])


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int, user: sqlite3.Row = Depends(current_user)
) -> dict[str, bool]:
    get_transaction(transaction_id, user["id"])
    connection = db()
    connection.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user["id"]),
    )
    connection.commit()
    connection.close()
    return {"deleted": True}


@app.get("/dashboard")
@app.get("/dashboard/summary", include_in_schema=False)
def dashboard(user: sqlite3.Row = Depends(current_user)) -> dict[str, Any]:
    connection = db()
    totals = connection.execute(
        """
        SELECT
          COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), 0)
            AS income,
          COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END), 0)
            AS expenses
        FROM transactions WHERE user_id = ?
        """,
        (user["id"],),
    ).fetchone()
    categories = connection.execute(
        """
        SELECT category, ROUND(SUM(amount), 2) AS total
        FROM transactions
        WHERE user_id = ? AND transaction_type = 'expense'
        GROUP BY category ORDER BY total DESC, category
        """,
        (user["id"],),
    ).fetchall()
    recent = connection.execute(
        """
        SELECT * FROM transactions WHERE user_id = ?
        ORDER BY transaction_date DESC, id DESC LIMIT 5
        """,
        (user["id"],),
    ).fetchall()
    connection.close()
    income = float(totals["income"])
    expenses = float(totals["expenses"])
    by_category = {row["category"]: float(row["total"]) for row in categories}
    return {
        "total_income": income,
        "total_expenses": expenses,
        "total_balance": income - expenses,
        "balance": income - expenses,
        "monthly_spend_by_category": by_category,
        "category_spending": by_category,
        "recent_transactions": [row_transaction(row) for row in recent],
    }