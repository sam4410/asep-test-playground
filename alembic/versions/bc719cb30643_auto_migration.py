"""Auto migration for Product, ShoppingCart, CartItem, and OrderHistory models."""

from alembic import op
import sqlalchemy as sa

revision = 'bc719cb30643'
down_revision = None

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
    )
    op.create_table(
        'shopping_carts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cart_id', sa.Integer(), sa.ForeignKey('shopping_carts.id'), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
    )
    op.create_table(
        'order_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('order_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
    )

def downgrade():
    op.drop_table('order_history')
    op.drop_table('cart_items')
    op.drop_table('shopping_carts')
    op.drop_table('products')