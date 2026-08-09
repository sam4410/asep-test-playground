"""Auto migration for User and Habit models.

Revision ID: 277919924735
Revises: None
"""

from alembic import op
import sqlalchemy as sa

revision = '277919924735'
down_revision = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

    # Create habits table
    op.create_table(
        'habits',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('name', sa.String, index=True),
        sa.Column('streak', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

def downgrade():
    # Drop habits table
    op.drop_table('habits')

    # Drop users table
    op.drop_table('users')