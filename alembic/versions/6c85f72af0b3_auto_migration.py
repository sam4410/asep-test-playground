"""Auto migration for Product model"""

from alembic import op
import sqlalchemy as sa
from api.models import Product  # Correct import for Product model

revision = '6c85f72af0b3'
down_revision = '3168776898c1'
branch_labels = None
depends_on = None

def upgrade():
    # Create the products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the products table
    op.drop_table('products')