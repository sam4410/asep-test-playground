"""Create User table

Revision ID: 1c58f62d53d2
Revises: None
Create Date: 2023-10-10 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '1c58f62d53d2'
down_revision = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('clerk_user_id', sa.String(), unique=True, index=True),
    )

def downgrade() -> None:
    op.drop_table('users')