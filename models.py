from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, FetchedValue, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (
        CheckConstraint("length(btrim(title)) > 0", name="ck_todos_title_not_blank"),
        Index("ix_todos_completed_created_at", "completed", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    completed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="false",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=FetchedValue(),
    )