"""Auto migration for Question model."""

from alembic import op
import sqlalchemy as sa

revision = '13e54b021e86'
down_revision = '5bb3474423de'

def upgrade():
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('question_text', sa.String, nullable=False),
        sa.Column('question_type', sa.String, nullable=False),  # e.g., 'multiple_choice', 'true_false', etc.
        sa.Column('options', sa.String, nullable=True),  # Store options as a comma-separated string
        sa.Column('correct_answer', sa.String, nullable=False),
        sa.Column('quiz_id', sa.Integer, sa.ForeignKey('quizzes.id')),  # Assuming a Quiz model exists
    )

def downgrade():
    op.drop_table('questions')