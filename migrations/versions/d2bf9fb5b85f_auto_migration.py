"""Create the todos table."""

from alembic import op
import sqlalchemy as sa


revision = "d2bf9fb5b85f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column(
            "completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "length(btrim(title)) > 0",
            name="ck_todos_title_not_blank",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todos_created_at", "todos", ["created_at"])
    op.create_index(
        "ix_todos_completed_created_at",
        "todos",
        ["completed", "created_at"],
    )
    op.execute(
        "CREATE OR REPLACE FUNCTION set_todos_updated_at() "
        "RETURNS TRIGGER LANGUAGE plpgsql AS $$ "
        "BEGIN NEW.updated_at = CURRENT_TIMESTAMP; "
        "RETURN NEW; END; $$"
    )
    op.execute(
        "CREATE TRIGGER todos_updated_at "
        "BEFORE UPDATE ON todos FOR EACH ROW "
        "EXECUTE FUNCTION set_todos_updated_at()"
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS todos_updated_at ON todos")
    op.execute("DROP FUNCTION IF EXISTS set_todos_updated_at()")
    op.drop_index("ix_todos_completed_created_at", table_name="todos")
    op.drop_index("ix_todos_created_at", table_name="todos")
    op.drop_table("todos")