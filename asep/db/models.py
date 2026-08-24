from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from uuid import uuid4

class HabitModel(Base):
    __tablename__ = "habits"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    habit_name: Mapped[str] = mapped_column(String(255), nullable=False)
    log_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    streak_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)