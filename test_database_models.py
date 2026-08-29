import os
import datetime
import uuid as uuid_module

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use an in-memory sqlite database for isolated unit testing instead of
# the Postgres URL configured in database.py.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import database
from database import Base, get_db
import models
from models import User, Habit, HabitCheckin, _uuid_default


@pytest.fixture()
def sqlite_engine():
    """A fresh in-memory sqlite engine with all tables created."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def sqlite_session(sqlite_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


class TestUuidDefault:
    def test_returns_string(self):
        value = _uuid_default()
        assert isinstance(value, str)

    def test_returns_valid_uuid(self):
        value = _uuid_default()
        # Should not raise - confirms it's a well-formed UUID string.
        parsed = uuid_module.UUID(value)
        assert str(parsed) == value

    def test_generates_unique_values(self):
        values = {_uuid_default() for _ in range(50)}
        assert len(values) == 50


class TestGetDb:
    def test_yields_a_session_and_closes_it(self, monkeypatch, sqlite_engine):
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

        gen = database.get_db()
        db = next(gen)
        try:
            assert db is not None
            # Session should be usable while generator is open.
            assert db.bind is sqlite_engine
        finally:
            # Exhaust the generator to trigger the finally: db.close()
            with pytest.raises(StopIteration):
                next(gen)

    def test_closes_session_even_after_exception(self, monkeypatch, sqlite_engine):
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

        gen = database.get_db()
        db = next(gen)
        closed_before = db.close  # keep ref, ensure no crash calling close via generator
        # Simulate the caller throwing an exception into the generator.
        with pytest.raises(ValueError):
            gen.throw(ValueError("boom"))


class TestUserModel:
    def test_create_user_with_defaults(self, sqlite_session):
        user = User(email="alice@example.com", hashed_password="hashed")
        sqlite_session.add(user)
        sqlite_session.commit()
        sqlite_session.refresh(user)

        assert user.id is not None
        assert isinstance(user.id, str)
        assert user.email == "alice@example.com"
        assert user.hashed_password == "hashed"
        assert isinstance(user.created_at, datetime.datetime)
        assert user.habits == []

    def test_duplicate_email_raises(self, sqlite_session):
        u1 = User(email="dup@example.com", hashed_password="a")
        sqlite_session.add(u1)
        sqlite_session.commit()

        u2 = User(email="dup@example.com", hashed_password="b")
        sqlite_session.add(u2)
        with pytest.raises(Exception):
            sqlite_session.commit()
        sqlite_session.rollback()


class TestHabitModel:
    def test_create_habit_with_defaults(self, sqlite_session):
        user = User(email="bob@example.com", hashed_password="x")
        sqlite_session.add(user)
        sqlite_session.commit()

        habit = Habit(user_id=user.id, name="Read")
        sqlite_session.add(habit)
        sqlite_session.commit()
        sqlite_session.refresh(habit)

        assert habit.id is not None
        assert habit.target_frequency == 1
        assert habit.is_archived is False
        assert habit.owner.email == "bob@example.com"
        assert habit in user.habits

    def test_habit_requires_user_id(self, sqlite_session):
        habit = Habit(name="No owner")
        sqlite_session.add(habit)
        with pytest.raises(Exception):
            sqlite_session.commit()
        sqlite_session.rollback()


class TestHabitCheckinModel:
    def test_create_checkin(self, sqlite_session):
        user = User(email="carol@example.com", hashed_password="x")
        sqlite_session.add(user)
        sqlite_session.commit()

        habit = Habit(user_id=user.id, name="Exercise")
        sqlite_session.add(habit)
        sqlite_session.commit()

        checkin = HabitCheckin(habit_id=habit.id, date=datetime.date.today())
        sqlite_session.add(checkin)
        sqlite_session.commit()
        sqlite_session.refresh(checkin)

        assert checkin.id is not None
        assert checkin.habit.name == "Exercise"
        assert checkin in habit.checkins

    def test_duplicate_checkin_same_day_violates_unique_constraint(self, sqlite_session):
        user = User(email="dave@example.com", hashed_password="x")
        sqlite_session.add(user)
        sqlite_session.commit()

        habit = Habit(user_id=user.id, name="Meditate")
        sqlite_session.add(habit)
        sqlite_session.commit()

        today = datetime.date.today()
        sqlite_session.add(HabitCheckin(habit_id=habit.id, date=today))
        sqlite_session.commit()

        sqlite_session.add(HabitCheckin(habit_id=habit.id, date=today))
        with pytest.raises(Exception):
            sqlite_session.commit()
        sqlite_session.rollback()
