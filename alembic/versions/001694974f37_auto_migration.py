"""Auto migration for Expense and Category models

Revision ID: 001694974f37
Revises: None
"""

from alembic import op
import sqlalchemy as sa

revision = '001694974f37'
down_revision = None

def upgrade():
    # Create expenses table
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )

def downgrade():
    # Drop categories table
    op.drop_table('categories')

    # Drop expenses table
    op.drop_table('expenses')