from datetime import datetime
from unittest.mock import Mock

import pytest

import database
from models import Todo


def test_get_db_yields_session_and_closes_it(monkeypatch):
    session = Mock()
    monkeypatch.setattr(database, "SessionLocal", lambda: session)

    db_generator = database.get_db()

    assert next(db_generator) is session
    with pytest.raises(StopIteration):
        next(db_generator)
    session.close.assert_called_once_with()


def test_get_db_closes_session_when_generator_is_closed(monkeypatch):
    session = Mock()
    monkeypatch.setattr(database, "SessionLocal", lambda: session)

    db_generator = database.get_db()
    assert next(db_generator) is session

    db_generator.close()

    session.close.assert_called_once_with()


def test_create_tables_creates_metadata_with_configured_engine(monkeypatch):
    create_all = Mock()
    monkeypatch.setattr(database.Base.metadata, "create_all", create_all)

    database.create_tables()

    create_all.assert_called_once_with(bind=database.engine)


def test_create_tables_propagates_metadata_error(monkeypatch):
    create_all = Mock(side_effect=RuntimeError("database unavailable"))
    monkeypatch.setattr(database.Base.metadata, "create_all", create_all)

    with pytest.raises(RuntimeError, match="database unavailable"):
        database.create_tables()


def test_create_db_and_tables_delegates_to_create_tables(monkeypatch):
    create_tables = Mock()
    monkeypatch.setattr(database, "create_tables", create_tables)

    assert database.create_db_and_tables() is None

    create_tables.assert_called_once_with()


def test_todo_metadata_defines_expected_columns_and_constraints():
    assert Todo.__tablename__ == "todos"
    assert set(Todo.__table__.columns.keys()) == {
        "id",
        "title",
        "description",
        "completed",
        "created_at",
    }
    assert Todo.__table__.c.id.primary_key
    assert not Todo.__table__.c.title.nullable
    assert Todo.__table__.c.description.nullable
    assert not Todo.__table__.c.completed.nullable
    assert not Todo.__table__.c.created_at.nullable


def test_todo_defaults_and_optional_description():
    todo = Todo(title="")

    assert todo.title == ""
    assert todo.description is None
    assert todo.__table__.c.completed.default.arg is False
    created_at = todo.__table__.c.created_at.default.arg(None)
    assert isinstance(created_at, datetime)
