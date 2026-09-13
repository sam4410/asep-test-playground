"""Create habit tracking data model.

Revision ID: 20260905_0001
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "20260905_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "anonymous_owners",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("stable_key", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("stable_key", name="uq_anonymous_owners_stable_key"),
    )
    op.create_index(
        "ix_anonymous_owners_stable_key",
        "anonymous_owners",
        ["stable_key"],
        unique=False,
    )

    op.create_table(
        "habit_templates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("default_schedule_type", sa.String(length=20), nullable=False),
        sa.Column("default_weekdays", sa.JSON(), nullable=True),
        sa.Column("default_interval_days", sa.Integer(), nullable=True),
        sa.Column(
            "default_missed_day_allowance",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "default_schedule_type IN "
            "('daily', 'weekly', 'weekdays', 'interval')",
            name="ck_habit_templates_schedule_type",
        ),
        sa.CheckConstraint(
            "default_missed_day_allowance >= 0",
            name="ck_habit_templates_allowance_nonnegative",
        ),
        sa.CheckConstraint(
            "default_interval_days IS NULL OR default_interval_days >= 1",
            name="ck_habit_templates_interval_positive",
        ),
        sa.UniqueConstraint("key", name="uq_habit_templates_key"),
    )
    op.create_index(
        "ix_habit_templates_is_active",
        "habit_templates",
        ["is_active"],
        unique=False,
    )
    op.bulk_insert(
        sa.table(
            "habit_templates",
            sa.column("id", sa.String()),
            sa.column("key", sa.String()),
            sa.column("name", sa.String()),
            sa.column("description", sa.Text()),
            sa.column("default_schedule_type", sa.String()),
            sa.column("default_weekdays", sa.JSON()),
            sa.column("default_interval_days", sa.Integer()),
            sa.column("default_missed_day_allowance", sa.Integer()),
            sa.column("is_active", sa.Boolean()),
        ),
        [
            {
                "id": "template-drink-water",
                "key": "drink_water",
                "name": "Drink Water",
                "description": "Track daily water intake.",
                "default_schedule_type": "daily",
                "default_weekdays": None,
                "default_interval_days": None,
                "default_missed_day_allowance": 1,
                "is_active": True,
            },
            {
                "id": "template-move-your-body",
                "key": "move_your_body",
                "name": "Move Your Body",
                "description": "Complete at least 20 minutes of physical activity.",
                "default_schedule_type": "daily",
                "default_weekdays": None,
                "default_interval_days": None,
                "default_missed_day_allowance": 1,
                "is_active": True,
            },
            {
                "id": "template-meditate",
                "key": "meditate",
                "name": "Meditate",
                "description": "Spend a few minutes on mindfulness or breathing exercises.",
                "default_schedule_type": "daily",
                "default_weekdays": None,
                "default_interval_days": None,
                "default_missed_day_allowance": 2,
                "is_active": True,
            },
            {
                "id": "template-read",
                "key": "read",
                "name": "Read",
                "description": "Read for at least 15 minutes.",
                "default_schedule_type": "daily",
                "default_weekdays": None,
                "default_interval_days": None,
                "default_missed_day_allowance": 2,
                "is_active": True,
            },
            {
                "id": "template-sleep-8-hours",
                "key": "sleep_8_hours",
                "name": "Sleep 8 Hours",
                "description": "Aim for a full night's sleep.",
                "default_schedule_type": "daily",
                "default_weekdays": None,
                "default_interval_days": None,
                "default_missed_day_allowance": 1,
                "is_active": True,
            },
            {
                "id": "template-weekly-planning",
                "key": "weekly_planning",
                "name": "Weekly Planning",
                "description": "Review goals and plan the upcoming week.",
                "default_schedule_type": "weekly",
                "default_weekdays": [6],
                "default_interval_days": None,
                "default_missed_day_allowance": 0,
                "is_active": True,
            },
        ],
    )

    op.create_table(
        "habits",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("anonymous_owner_id", sa.String(length=36), nullable=True),
        sa.Column("stable_identifier", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_predefined", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("predefined_key", sa.String(length=100), nullable=True),
        sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["anonymous_owner_id"], ["anonymous_owners.id"]),
        sa.CheckConstraint(
            "(user_id IS NOT NULL AND anonymous_owner_id IS NULL) OR "
            "(user_id IS NULL AND anonymous_owner_id IS NOT NULL)",
            name="ck_habit_single_owner",
        ),
    )
    op.create_index("ix_habits_user_id", "habits", ["user_id"], unique=False)
    op.create_index(
        "ix_habits_anonymous_owner_id",
        "habits",
        ["anonymous_owner_id"],
        unique=False,
    )
    op.create_index(
        "ix_habits_user_stable_identifier",
        "habits",
        ["user_id", "stable_identifier"],
        unique=False,
    )
    op.create_index(
        "ix_habits_anonymous_stable_identifier",
        "habits",
        ["anonymous_owner_id", "stable_identifier"],
        unique=False,
    )
    op.create_index(
        "ix_habits_predefined_key",
        "habits",
        ["predefined_key"],
        unique=False,
    )
    op.create_index("ix_habits_archived", "habits", ["archived"], unique=False)

    op.create_table(
        "habit_schedule_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("habit_id", sa.String(length=36), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("schedule_type", sa.String(length=20), nullable=False),
        sa.Column("weekdays", sa.JSON(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=True),
        sa.Column("anchor_date", sa.Date(), nullable=True),
        sa.Column("missed_day_allowance", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"]),
        sa.CheckConstraint(
            "schedule_type IN ('daily', 'weekly', 'weekdays', 'interval')",
            name="ck_habit_schedule_type",
        ),
        sa.CheckConstraint(
            "missed_day_allowance >= 0",
            name="ck_habit_schedule_nonnegative_allowance",
        ),
        sa.CheckConstraint(
            "interval_days IS NULL OR interval_days >= 1",
            name="ck_habit_schedule_positive_interval",
        ),
        sa.UniqueConstraint(
            "habit_id",
            "effective_from",
            name="uq_habit_schedule_version_start",
        ),
    )
    op.create_index(
        "ix_habit_schedule_versions_habit_id",
        "habit_schedule_versions",
        ["habit_id"],
        unique=False,
    )
    op.create_index(
        "ix_habit_schedule_versions_habit_date",
        "habit_schedule_versions",
        ["habit_id", "effective_from"],
        unique=False,
    )

    op.create_table(
        "habit_completions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("habit_id", sa.String(length=36), nullable=False),
        sa.Column("completion_date", sa.Date(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("modified_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"]),
        sa.UniqueConstraint(
            "habit_id",
            "completion_date",
            name="uq_habit_completion_date",
        ),
    )
    op.create_index(
        "ix_habit_completions_habit_id",
        "habit_completions",
        ["habit_id"],
        unique=False,
    )
    op.create_index(
        "ix_habit_completions_habit_date",
        "habit_completions",
        ["habit_id", "completion_date"],
        unique=False,
    )

    op.create_table(
        "habit_streaks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("habit_id", sa.String(length=36), nullable=False),
        sa.Column("current_completed_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_calendar_span", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest_completed_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest_calendar_span", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("calculated_through", sa.Date(), nullable=True),
        sa.Column("calculation_inputs", sa.JSON(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"]),
        sa.UniqueConstraint("habit_id", name="uq_habit_streak_habit"),
        sa.CheckConstraint(
            "current_completed_days >= 0 AND current_calendar_span >= 0 AND "
            "longest_completed_days >= 0 AND longest_calendar_span >= 0",
            name="ck_habit_streak_nonnegative_values",
        ),
    )
    op.create_index(
        "ix_habit_streaks_habit_id",
        "habit_streaks",
        ["habit_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_habit_streaks_habit_id", table_name="habit_streaks")
    op.drop_table("habit_streaks")

    op.drop_index("ix_habit_completions_habit_date", table_name="habit_completions")
    op.drop_index("ix_habit_completions_habit_id", table_name="habit_completions")
    op.drop_table("habit_completions")

    op.drop_index(
        "ix_habit_schedule_versions_habit_date",
        table_name="habit_schedule_versions",
    )
    op.drop_index(
        "ix_habit_schedule_versions_habit_id",
        table_name="habit_schedule_versions",
    )
    op.drop_table("habit_schedule_versions")

    op.drop_index("ix_habits_archived", table_name="habits")
    op.drop_index("ix_habits_predefined_key", table_name="habits")
    op.drop_index("ix_habits_anonymous_stable_identifier", table_name="habits")
    op.drop_index("ix_habits_user_stable_identifier", table_name="habits")
    op.drop_index("ix_habits_anonymous_owner_id", table_name="habits")
    op.drop_index("ix_habits_user_id", table_name="habits")
    op.drop_table("habits")

    op.drop_index("ix_habit_templates_is_active", table_name="habit_templates")
    op.drop_table("habit_templates")

    op.drop_index("ix_anonymous_owners_stable_key", table_name="anonymous_owners")
    op.drop_table("anonymous_owners")