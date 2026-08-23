"""Auto migration for Habit model"""

from alembic import op
import sqlalchemy as sa

revision = '3168776898c1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create the habits table
    op.create_table(
        'habits',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('streak_count', sa.Integer(), nullable=True, default=0),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the habits table
    op.drop_table('habits')

import sys
sys.path.insert(0, '/path/to/your/api')  # Adjust the path to your api module