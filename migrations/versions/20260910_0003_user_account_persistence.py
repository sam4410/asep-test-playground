"""enforce normalized user account email addresses

Revision ID: 20260910_0003_user_account_persistence
Revises: 0001_create_recipe_and_user_models
Create Date: 2026-09-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260910_0003_user_account_persistence"
down_revision = "0001_create_recipe_and_user_models"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("UPDATE users SET email = lower(trim(email))"))

    with op.batch_alter_table("users") as batch_op:
        batch_op.create_check_constraint(
            "ck_users_email_normalized",
            "email = lower(trim(email))",
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(
            "ck_users_email_normalized",
            type_="check",
        )
