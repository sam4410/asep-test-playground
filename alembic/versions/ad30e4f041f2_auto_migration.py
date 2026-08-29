"""auto migration: create users, habits, habit_checkins tables

Revision ID: ad30e4f041f2
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ad30e4f041f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'habits',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('target_frequency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_archived', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()'),
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk_habits_user_id_users'), ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_habits')),
    )
    op.create_index(op.f('ix_habits_user_id'), 'habits', ['user_id'], unique=False)
    op.create_index('habits_user_id_idx', 'habits', ['user_id'], unique=False)
    op.create_index('habits_is_archived_idx', 'habits', ['is_archived'], unique=False)

    op.create_table(
        'habit_checkins',
        sa.Column('id', postgresql.UUID(as_uuid=False), primary_key=True, nullable=False),
        sa.Column('habit_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()'),
        ),
        sa.ForeignKeyConstraint(
            ['habit_id'], ['habits.id'], name=op.f('fk_habit_checkins_habit_id_habits'), ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_habit_checkins')),
        sa.UniqueConstraint('habit_id', 'date', name='habit_checkins_habit_date_uidx'),
    )
    op.create_index(op.f('ix_habit_checkins_habit_id'), 'habit_checkins', ['habit_id'], unique=False)
    op.create_index('habit_checkins_date_idx', 'habit_checkins', ['date'], unique=False)


def downgrade():
    op.drop_index('habit_checkins_date_idx', table_name='habit_checkins')
    op.drop_index(op.f('ix_habit_checkins_habit_id'), table_name='habit_checkins')
    op.drop_table('habit_checkins')

    op.drop_index('habits_is_archived_idx', table_name='habits')
    op.drop_index('habits_user_id_idx', table_name='habits')
    op.drop_index(op.f('ix_habits_user_id'), table_name='habits')
    op.drop_table('habits')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')