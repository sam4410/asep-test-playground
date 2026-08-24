"""Auto migration for User, Quiz, and QuizSubmission models."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = '5bb3474423de'
down_revision = 'bc719cb30643'

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('username', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
    )

    op.create_table(
        'quizzes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('teacher_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column('questions', JSONB, nullable=False),
    )

    op.create_table(
        'quiz_submissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('quiz_id', UUID(as_uuid=True), sa.ForeignKey('quizzes.id'), nullable=False),
        sa.Column('student_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('answers', JSONB, nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    )

def downgrade():
    op.drop_table('quiz_submissions')
    op.drop_table('quizzes')
    op.drop_table('users')