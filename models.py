import uuid
import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


def _uuid_default():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid_default)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid_default)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    target_frequency = Column(Integer, nullable=False, default=1)
    is_archived = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="habits")
    checkins = relationship("HabitCheckin", back_populates="habit", cascade="all, delete-orphan")

    __table_args__ = (
        Index("habits_user_id_idx", "user_id"),
        Index("habits_is_archived_idx", "is_archived"),
    )


class HabitCheckin(Base):
    __tablename__ = "habit_checkins"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid_default)
    habit_id = Column(UUID(as_uuid=False), ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="checkins")

    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="habit_checkins_habit_date_uidx"),
        Index("habit_checkins_date_idx", "date"),
    )