"""Auto migration for HabitModel."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'f52f098b8e40'
down_revision = 'bc719cb30643'

def upgrade():
    op.create_table(
        'habits',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('habit_name', sa.String(length=255), nullable=False),
        sa.Column('log_date', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('streak_count', sa.Integer(), nullable=False, default=0),
    )

def downgrade():
    op.drop_table('habits')
