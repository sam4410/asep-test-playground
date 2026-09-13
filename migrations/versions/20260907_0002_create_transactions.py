"""Create personal finance transactions.

Revision ID: 20260907_0002
Revises: 0001_create_recipe_and_user_models
"""

from alembic import op
import sqlalchemy as sa


revision = "20260907_0002"
down_revision = "0001_create_recipe_and_user_models"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "transactions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("transaction_type", sa.String(length=7), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "transaction_type IN ('income', 'expense')",
            name="ck_transactions_type",
        ),
        sa.CheckConstraint(
            "amount_cents >= 0",
            name="ck_transactions_amount_cents_nonnegative",
        ),
    )
    op.create_index(
        "ix_transactions_user_id",
        "transactions",
        ["user_id"],
    )
    op.create_index(
        "ix_transactions_transaction_date",
        "transactions",
        ["transaction_date"],
    )
    op.create_index(
        "ix_transactions_user_date",
        "transactions",
        ["user_id", "transaction_date"],
    )
    op.create_index(
        "ix_transactions_user_type",
        "transactions",
        ["user_id", "transaction_type"],
    )


def downgrade():
    op.drop_index("ix_transactions_user_type", table_name="transactions")
    op.drop_index("ix_transactions_user_date", table_name="transactions")
    op.drop_index("ix_transactions_transaction_date", table_name="transactions")
    op.drop_index("ix_transactions_user_id", table_name="transactions")
    op.drop_table("transactions")
