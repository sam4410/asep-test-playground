"""Auto migration for Note model"""

from alembic import op
import sqlalchemy as sa

revision = 'ad481de4cc1e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create the notes table
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the notes table
    op.drop_table('notes')