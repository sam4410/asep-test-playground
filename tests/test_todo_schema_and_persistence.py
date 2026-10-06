from datetime import datetime
from datetime import timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from models import Todo
from schemas import TodoCreate
from schemas import TodoResponse
from schemas import TodoUpdate


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_todo_create_schema_applies_defaults_and_strips_title():
    todo = TodoCreate.model_validate({"title": "  Buy milk  "})

    assert todo.title == "Buy milk"
    assert todo.description is None
    assert todo.completed is False


def test_todo_create_schema_accepts_description_and_completed_true():
    todo = TodoCreate.model_validate(
        {
            "title": "Write tests",
            "description": "Cover schema behavior",
            "completed": True,
        }
    )

    assert todo.description == "Cover schema behavior"
    assert todo.completed is True


@pytest.mark.parametrize("title", ["", "   "])
def test_todo_create_schema_rejects_empty_titles(title):
    with pytest.raises(ValidationError):
        TodoCreate.model_validate({"title": title})


def test_todo_create_schema_rejects_non_boolean_completed_values():
    with pytest.raises(ValidationError):
        TodoCreate.model_validate({"title": "Use strict booleans", "completed": 1})


def test_todo_update_schema_supports_partial_completed_update():
    todo = TodoUpdate.model_validate({"completed": True})

    assert todo.title is None
    assert todo.description is None
    assert todo.completed is True
    assert todo.model_dump(exclude_unset=True) == {"completed": True}


def test_todo_update_schema_rejects_empty_title():
    with pytest.raises(ValidationError):
        TodoUpdate.model_validate({"title": "  "})


def test_todo_model_sets_created_at_and_completed_defaults_on_persist(db_session):
    before = datetime.utcnow() - timedelta(seconds=1)
    todo = Todo(title="Persist defaults")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    after = datetime.utcnow() + timedelta(seconds=1)

    assert todo.completed is False
    assert todo.created_at is not None
    assert before <= todo.created_at <= after


def test_todo_model_persists_all_fields_and_can_be_loaded(db_session):
    created_at = datetime(2025, 1, 2, 3, 4, 5)
    todo = Todo(
        title="Persisted todo",
        description="Stored description",
        completed=True,
        created_at=created_at,
    )
    db_session.add(todo)
    db_session.commit()
    todo_id = todo.id
    db_session.expunge_all()

    loaded = db_session.get(Todo, todo_id)

    assert loaded is not None
    assert loaded.title == "Persisted todo"
    assert loaded.description == "Stored description"
    assert loaded.completed is True
    assert loaded.created_at == created_at


def test_todo_response_serializes_persisted_model_fields(db_session):
    todo = Todo(title="Response todo", completed=False)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    response = TodoResponse.model_validate(todo)

    assert response.id == todo.id
    assert response.title == "Response todo"
    assert response.description is None
    assert response.completed is False
    assert response.created_at == todo.created_at

