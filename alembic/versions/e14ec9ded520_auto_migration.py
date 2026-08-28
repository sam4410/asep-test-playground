"""auto migration

Revision ID: e14ec9ded520
Revises: None
Create Date: 2023-10-10 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = 'e14ec9ded520'
down_revision = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('clerk_user_id', sa.String(), unique=True, index=True)
    )

    # Create invoices table
    op.create_table(
        'invoices',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), index=True),
        sa.Column('client_name', sa.String(), index=True),
        sa.Column('amount', sa.Integer()),
        sa.Column('status', sa.String())  # 'paid' or 'unpaid'
    )

def downgrade():
    # Drop invoices table
    op.drop_table('invoices')

    # Drop users table
    op.drop_table('users')