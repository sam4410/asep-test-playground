"""Create habit tracking metadata and historical calculation inputs.

Revision ID: 20260905_02
Revises: 20260905_01
"""
from datetime import datetime, timezone
import sqlalchemy as sa
from alembic import op

revision = "20260905_02"
down_revision = "20260905_01"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "habit_templates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("default_schedule_type", sa.String(length=20), nullable=False),
        sa.Column("default_weekdays", sa.JSON(), nullable=True),
        sa.Column("default_interval_days", sa.Integer(), nullable=True),
        sa.Column("default_missed_day_allowance", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("default_schedule_type IN ('daily', 'weekly', 'custom')", name="ck_habit_templates_schedule_type"),
        sa.CheckConstraint("default_missed_day_allowance >= 0", name="ck_habit_templates_allowance_nonnegative"),
        sa.CheckConstraint("default_interval_days IS NULL OR default_interval_days >= 1", name="ck_habit_templates_interval_positive"),
        sa.UniqueConstraint("key", name="uq_habit_templates_key"),
    )
    op.create_index("ix_habit_templates_is_active", "habit_templates", ["is_active"])
    op.add_column("habits", sa.Column("stable_id", sa.String(length=36), nullable=True))
    op.add_column("habits", sa.Column("template_id", sa.String(length=36), nullable=True))
    op.add_column("habits", sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("habits", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column("habits", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_foreign_key("fk_habits_template_id", "habits", "habit_templates", ["template_id"], ["id"])
    op.create_index("ix_habits_stable_id", "habits", ["stable_id"])
    op.create_index("ix_habits_owner_archived", "habits", ["user_id", "is_archived"])
    op.create_index("uq_habits_owner_stable_id", "habits", ["user_id", "stable_id"], unique=True)
    op.create_table(
        "habit_schedule_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("schedule_type", sa.String(length=20), nullable=False),
        sa.Column("weekdays", sa.JSON(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=True),
        sa.Column("anchor_date", sa.Date(), nullable=True),
        sa.Column("missed_day_allowance", sa.Integer(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], name="fk_habit_schedule_versions_habit_id", ondelete="CASCADE"),
        sa.CheckConstraint("schedule_type IN ('daily', 'weekly', 'custom')", name="ck_habit_schedule_versions_type"),
        sa.CheckConstraint("missed_day_allowance >= 0", name="ck_habit_schedule_versions_allowance"),
        sa.CheckConstraint("interval_days IS NULL OR interval_days >= 1", name="ck_habit_schedule_versions_interval"),
        sa.UniqueConstraint("habit_id", "effective_from", name="uq_habit_schedule_versions_habit_date"),
    )
    op.create_index("ix_habit_schedule_versions_habit_effective", "habit_schedule_versions", ["habit_id", "effective_from"])
    op.create_table(
        "habit_completions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], name="fk_habit_completions_habit_id", ondelete="CASCADE"),
        sa.UniqueConstraint("habit_id", "entry_date", name="uq_habit_completions_habit_date"),
    )
    op.create_index("ix_habit_completions_habit_date", "habit_completions", ["habit_id", "entry_date"])
    op.create_table(
        "habit_streaks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("current_completed_days", sa.Integer(), nullable=False),
        sa.Column("current_calendar_span_days", sa.Integer(), nullable=False),
        sa.Column("longest_completed_days", sa.Integer(), nullable=False),
        sa.Column("longest_calendar_span_days", sa.Integer(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], name="fk_habit_streaks_habit_id", ondelete="CASCADE"),
        sa.CheckConstraint("current_completed_days >= 0", name="ck_habit_streaks_current_completed"),
        sa.CheckConstraint("current_calendar_span_days >= 0", name="ck_habit_streaks_current_span"),
        sa.CheckConstraint("longest_completed_days >= 0", name="ck_habit_streaks_longest_completed"),
        sa.CheckConstraint("longest_calendar_span_days >= 0", name="ck_habit_streaks_longest_span"),
        sa.UniqueConstraint("habit_id", name="uq_habit_streaks_habit"),
    )
    op.create_index("ix_habit_streaks_habit_id", "habit_streaks", ["habit_id"])
    templates = sa.table(
        "habit_templates",
        sa.column("id", sa.String(length=36)),
        sa.column("key", sa.String(length=100)),
        sa.column("name", sa.String(length=255)),
        sa.column("description", sa.Text()),
        sa.column("default_schedule_type", sa.String(length=20)),
        sa.column("default_weekdays", sa.JSON()),
        sa.column("default_interval_days", sa.Integer()),
        sa.column("default_missed_day_allowance", sa.Integer()),
        sa.column("is_active", sa.Boolean()),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    created_at = datetime.now(timezone.utc)
    op.bulk_insert(templates, [
        {"id": "template-drink-water", "key": "drink-water", "name": "Drink Water", "description": "Track daily water intake", "default_schedule_type": "daily", "default_weekdays": None, "default_interval_days": None, "default_missed_day_allowance": 1, "is_active": True, "created_at": created_at},
        {"id": "template-move-your-body", "key": "move-your-body", "name": "Move Your Body", "description": "Complete at least 20 minutes of physical activity", "default_schedule_type": "daily", "default_weekdays": None, "default_interval_days": None, "default_missed_day_allowance": 1, "is_active": True, "created_at": created_at},
        {"id": "template-meditate", "key": "meditate", "name": "Meditate", "description": "Spend a few minutes on mindfulness or breathing exercises", "default_schedule_type": "daily", "default_weekdays": None, "default_interval_days": None, "default_missed_day_allowance": 2, "is_active": True, "created_at": created_at},
        {"id": "template-read", "key": "read", "name": "Read", "description": "Read for at least 15 minutes", "default_schedule_type": "daily", "default_weekdays": None, "default_interval_days": None, "default_missed_day_allowance": 2, "is_active": True, "created_at": created_at},
        {"id": "template-sleep-eight-hours", "key": "sleep-eight-hours", "name": "Sleep 8 Hours", "description": "Aim for a full night's sleep", "default_schedule_type": "daily", "default_weekdays": None, "default_interval_days": None, "default_missed_day_allowance": 1, "is_active": True, "created_at": created_at},
        {"id": "template-weekly-planning", "key": "weekly-planning", "name": "Weekly Planning", "description": "Review goals and plan the upcoming week", "default_schedule_type": "weekly", "default_weekdays": [6], "default_interval_days": None, "default_missed_day_allowance": 0, "is_active": True, "created_at": created_at},
    ])
def downgrade():
    op.drop_index("ix_habit_streaks_habit_id", table_name="habit_streaks")
    op.drop_table("habit_streaks")
    op.drop_index("ix_habit_completions_habit_date", table_name="habit_completions")
    op.drop_table("habit_completions")
    op.drop_index("ix_habit_schedule_versions_habit_effective", table_name="habit_schedule_versions")
    op.drop_table("habit_schedule_versions")
    op.drop_index("uq_habits_owner_stable_id", table_name="habits")
    op.drop_index("ix_habits_owner_archived", table_name="habits")
    op.drop_index("ix_habits_stable_id", table_name="habits")
    op.drop_constraint("fk_habits_template_id", "habits", type_="foreignkey")
    op.drop_column("habits", "updated_at")
    op.drop_column("habits", "created_at")
    op.drop_column("habits", "is_archived")
    op.drop_column("habits", "template_id")
    op.drop_column("habits", "stable_id")
    op.drop_index("ix_habit_templates_is_active", table_name="habit_templates")
    op.drop_table("habit_templates")