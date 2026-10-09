import importlib
import os

from sqlalchemy import CheckConstraint, Index
from sqlalchemy.schema import FetchedValue


def test_todo_mapping_defines_expected_columns_and_constraints(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/todos",
    )
    models = importlib.import_module("models")
    todo = models.Todo
    table = todo.__table__

    assert todo.__tablename__ == "todos"
    assert list(table.columns.keys()) == [
        "id",
        "title",
        "completed",
        "created_at",
        "updated_at",
    ]
    assert table.c.id.primary_key
    assert table.c.title.type.length == 500
    assert table.c.title.nullable is False
    assert table.c.completed.nullable is False
    assert table.c.created_at.nullable is False
    assert table.c.updated_at.nullable is False

    constraints = {
        constraint.name
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }
    assert "ck_todos_title_not_blank" in constraints

    indexes = {
        index.name: tuple(column.name for column in index.columns)
        for index in table.indexes
        if isinstance(index, Index)
    }
    assert indexes["ix_todos_created_at"] == ("created_at",)
    assert indexes["ix_todos_completed_created_at"] == (
        "completed",
        "created_at",
    )


def test_todo_defaults_and_update_metadata_are_configured(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/todos",
    )
    models = importlib.import_module("models")
    table = models.Todo.__table__

    assert table.c.completed.default.arg is False
    assert str(table.c.created_at.default.arg) == "now()"
    assert str(table.c.created_at.server_default.arg) == "now()"
    assert str(table.c.updated_at.default.arg) == "now()"
    assert str(table.c.updated_at.onupdate.arg) == "now()"
    assert isinstance(table.c.updated_at.server_onupdate, FetchedValue)

    todo = models.Todo(title="Write tests")
    assert todo.title == "Write tests"
    assert todo.completed is None
