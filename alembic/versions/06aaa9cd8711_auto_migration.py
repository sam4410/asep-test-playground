"""Auto migration for Task model"""

from alembic import op
import sqlalchemy as sa

revision = '06aaa9cd8711'
down_revision = '3168776898c1'
branch_labels = None
depends_on = None

def upgrade():
    # Create the tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(), index=True),
        sa.Column('description', sa.String()),
        sa.Column('assignee_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('status', sa.Enum('todo', 'in_progress', 'done', name='taskstatus'), 
                  nullable=False, server_default='todo'),
        sa.Column('created_at', sa.DateTime(), nullable=False),  # Use appropriate type for timestamps
        sa.Column('updated_at', sa.DateTime(), nullable=False)   # Use appropriate type for timestamps
    )

def downgrade():
    # Drop the tasks table
    op.drop_table('tasks')
