from __future__ import annotations

import os
from urllib.parse import urlparse, unquote

# Set environment variables BEFORE importing any app code
db_url = os.environ.get("DATABASE_URL", "postgresql+psycopg://postgres:admin%40123@localhost:5432/asep")
parsed = urlparse(db_url.replace("postgresql+psycopg://", "postgresql://"))
host = parsed.hostname or "localhost"
port = parsed.port or 5432
raw_user = parsed.username or "postgres"
raw_pass = parsed.password or "admin%40123"
admin_db = parsed.path.lstrip("/") or "postgres"

test_db_name = "asep_test"
# Keep password URL-encoded for SQLAlchemy and Alembic connection string
os.environ["DATABASE_URL"] = f"postgresql+psycopg://{raw_user}:{raw_pass}@{host}:{port}/{test_db_name}"
os.environ["ASEP_MAX_TASK_RETRIES"] = "1"

import pytest
import psycopg
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from asep.db.base import Base

# Unquote credentials for the direct psycopg DSN connection parameters
user = unquote(raw_user)
password = unquote(raw_pass)
admin_dsn = f"host={host} port={port} user={user} password={password} dbname={admin_db}"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Connect to postgres server to create test db
    conn = psycopg.connect(admin_dsn, autocommit=True)
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)")
        cur.execute(f"CREATE DATABASE {test_db_name}")
    conn.close()

    # Run migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    # Dispose of the SQLAlchemy connection pool to close all active connections
    try:
        from asep.db.session import get_engine
        get_engine().dispose()
    except Exception:
        pass

    # Clean up test database
    conn = psycopg.connect(admin_dsn, autocommit=True)
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)")
    conn.close()

@pytest.fixture(autouse=True)
def clean_db():
    from asep.db.session import get_engine
    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(
            sa.text("TRUNCATE TABLE runs, tasks, task_dependencies, task_artifacts, memory_records, events, agent_results CASCADE")
        )

