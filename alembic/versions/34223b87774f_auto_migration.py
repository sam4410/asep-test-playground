"""Auto migration for Quiz, Question, and Answer models

Revision ID: 34223b87774f
Revises: 001694974f37
"""

from alembic import op
import sqlalchemy as sa

revision = '34223b87774f'
down_revision = '001694974f37'

def upgrade():
    # Create quizzes table
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('title', sa.String(), index=True),
        sa.Column('teacher_id', sa.Integer(), sa.ForeignKey('teachers.id'))
    )

    # Create questions table
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('quizzes.id')),
        sa.Column('text', sa.String()),
        sa.Column('correct_answer_id', sa.Integer(), sa.ForeignKey('answers.id'))
    )

    # Create answers table
    op.create_table(
        'answers',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('question_id', sa.Integer(), sa.ForeignKey('questions.id')),
        sa.Column('text', sa.String())
    )

def downgrade():
    # Drop answers table
    op.drop_table('answers')

    # Drop questions table
    op.drop_table('questions')

    # Drop quizzes table
    op.drop_table('quizzes')