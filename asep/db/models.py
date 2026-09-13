import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    CheckConstraint,
    Date,
    JSON,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Float,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=_uuid)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    recipes = relationship(
        "Recipe", back_populates="owner", cascade="all, delete-orphan"
    )
    habits = relationship(
        "Habit", back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    dietary_tags = Column(JSON, nullable=True, default=list)
    allergens = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    owner = relationship("User", back_populates="recipes")
    ingredients = relationship(
        "Ingredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    steps = relationship(
        "RecipeStep",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.order",
    )

    def __repr__(self):
        return f"<Recipe {self.name}>"


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(String(36), primary_key=True, default=_uuid)
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient {self.name}>"


class RecipeStep(Base):
    __tablename__ = "recipe_steps"

    id = Column(String(36), primary_key=True, default=_uuid)
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=False, index=True)
    order = Column(Integer, nullable=False, default=0)
    instruction = Column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="steps")

    def __repr__(self):
        return f"<RecipeStep {self.order}: {self.instruction[:20]}>"


class AnonymousOwner(Base):
    """Stable ownership record for data created before account registration."""

    __tablename__ = "anonymous_owners"

    id = Column(String(36), primary_key=True, default=_uuid)
    stable_key = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habits = relationship(
        "Habit",
        back_populates="anonymous_owner",
        cascade="all, delete-orphan",
    )


class HabitTemplate(Base):
    """Metadata for a predefined habit in the launch habit library."""

    __tablename__ = "habit_templates"
    __table_args__ = (
        CheckConstraint(
            "default_schedule_type IN "
            "('daily', 'weekly', 'weekdays', 'interval')",
            name="ck_habit_templates_schedule_type",
        ),
        CheckConstraint(
            "default_missed_day_allowance >= 0",
            name="ck_habit_templates_allowance_nonnegative",
        ),
        CheckConstraint(
            "default_interval_days IS NULL OR default_interval_days >= 1",
            name="ck_habit_templates_interval_positive",
        ),
        UniqueConstraint("key", name="uq_habit_templates_key"),
        Index("ix_habit_templates_is_active", "is_active"),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    key = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    default_schedule_type = Column(String(20), nullable=False)
    default_weekdays = Column(JSON, nullable=True)
    default_interval_days = Column(Integer, nullable=True)
    default_missed_day_allowance = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Habit(Base):
    __tablename__ = "habits"
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND anonymous_owner_id IS NULL) OR "
            "(user_id IS NULL AND anonymous_owner_id IS NOT NULL)",
            name="ck_habit_single_owner",
        ),
        Index(
            "ix_habits_user_stable_identifier",
            "user_id",
            "stable_identifier",
        ),
        Index(
            "ix_habits_anonymous_stable_identifier",
            "anonymous_owner_id",
            "stable_identifier",
        ),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    anonymous_owner_id = Column(
        String(36),
        ForeignKey("anonymous_owners.id"),
        nullable=True,
        index=True,
    )
    stable_identifier = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_predefined = Column(Boolean, nullable=False, default=False)
    predefined_key = Column(String(100), nullable=True, index=True)
    archived = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    owner = relationship("User", back_populates="habits")
    anonymous_owner = relationship("AnonymousOwner", back_populates="habits")
    schedule_versions = relationship(
        "HabitScheduleVersion",
        back_populates="habit",
        cascade="all, delete-orphan",
        order_by="HabitScheduleVersion.effective_from",
    )
    completions = relationship(
        "HabitCompletion",
        back_populates="habit",
        cascade="all, delete-orphan",
    )
    streak = relationship(
        "HabitStreak",
        back_populates="habit",
        uselist=False,
        cascade="all, delete-orphan",
    )


class HabitScheduleVersion(Base):
    """Schedule and allowance effective from a UTC calendar date onward."""

    __tablename__ = "habit_schedule_versions"
    __table_args__ = (
        CheckConstraint(
            "schedule_type IN ('daily', 'weekly', 'weekdays', 'interval')",
            name="ck_habit_schedule_type",
        ),
        CheckConstraint(
            "missed_day_allowance >= 0",
            name="ck_habit_schedule_nonnegative_allowance",
        ),
        CheckConstraint(
            "interval_days IS NULL OR interval_days >= 1",
            name="ck_habit_schedule_positive_interval",
        ),
        UniqueConstraint(
            "habit_id",
            "effective_from",
            name="uq_habit_schedule_version_start",
        ),
        Index(
            "ix_habit_schedule_versions_habit_date",
            "habit_id",
            "effective_from",
        ),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    habit_id = Column(
        String(36),
        ForeignKey("habits.id"),
        nullable=False,
        index=True,
    )
    effective_from = Column(Date, nullable=False, default=date.today)
    schedule_type = Column(String(20), nullable=False)
    weekdays = Column(JSON, nullable=True)
    interval_days = Column(Integer, nullable=True)
    anchor_date = Column(Date, nullable=True)
    missed_day_allowance = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="schedule_versions")


class HabitCompletion(Base):
    __tablename__ = "habit_completions"
    __table_args__ = (
        UniqueConstraint(
            "habit_id",
            "completion_date",
            name="uq_habit_completion_date",
        ),
        Index(
            "ix_habit_completions_habit_date",
            "habit_id",
            "completion_date",
        ),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    habit_id = Column(
        String(36),
        ForeignKey("habits.id"),
        nullable=False,
        index=True,
    )
    completion_date = Column(Date, nullable=False)
    completed = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    habit = relationship("Habit", back_populates="completions")


class HabitStreak(Base):
    """Persisted streak values and the schedule inputs used to calculate them."""

    __tablename__ = "habit_streaks"
    __table_args__ = (
        CheckConstraint(
            "current_completed_days >= 0 AND "
            "current_calendar_span >= 0 AND "
            "longest_completed_days >= 0 AND "
            "longest_calendar_span >= 0",
            name="ck_habit_streak_nonnegative_values",
        ),
    )

    id = Column(String(36), primary_key=True, default=_uuid)
    habit_id = Column(
        String(36),
        ForeignKey("habits.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    current_completed_days = Column(Integer, nullable=False, default=0)
    current_calendar_span = Column(Integer, nullable=False, default=0)
    longest_completed_days = Column(Integer, nullable=False, default=0)
    longest_calendar_span = Column(Integer, nullable=False, default=0)
    calculated_through = Column(Date, nullable=True)
    calculation_inputs = Column(JSON, nullable=False, default=dict)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="streak")
