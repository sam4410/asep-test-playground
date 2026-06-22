from __future__ import annotations

import os
# Set environment variables BEFORE importing any app code
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:admin%40123@localhost:5432/asep_test"
os.environ["ASEP_MAX_TASK_RETRIES"] = "1"

import pytest
import psycopg
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from asep.db.base import Base


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Connect to default postgres to create test db
    conn = psycopg.connect("host=localhost port=5432 user=postgres password=admin@123", autocommit=True)
    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS asep_test WITH (FORCE)")
        cur.execute("CREATE DATABASE asep_test")
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
    conn = psycopg.connect("host=localhost port=5432 user=postgres password=admin@123", autocommit=True)
    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS asep_test WITH (FORCE)")
    conn.close()

@pytest.fixture(autouse=True)
def clean_db():
    from asep.db.session import get_engine
    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(
            sa.text("TRUNCATE TABLE runs, tasks, task_dependencies, task_artifacts, memory_records, events, agent_results CASCADE")
        )

