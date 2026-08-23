"""Auto migration for Product model

Revision ID: dd0b46af2eb2
Revises: 001694974f37
"""

from alembic import op
import sqlalchemy as sa
import sys
import os

revision = 'dd0b46af2eb2'
down_revision = '001694974f37'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
def upgrade():
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=False)
    )

def downgrade():
    # Drop products table
    op.drop_table('products')