"""create recipe and user models

Revision ID: 0001_create_recipe_and_user_models
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "0001_create_recipe_and_user_models"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table(
        "recipes",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("dietary_tags", sa.JSON(), nullable=True),
        sa.Column("allergens", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("ix_recipes_user_id", "recipes", ["user_id"])

    op.create_table(
        "ingredients",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("recipe_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"]),
    )
    op.create_index("ix_ingredients_recipe_id", "ingredients", ["recipe_id"])
    op.create_index("ix_ingredients_name", "ingredients", ["name"])

    op.create_table(
        "recipe_steps",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("recipe_id", sa.String(length=36), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("instruction", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"]),
    )
    op.create_index("ix_recipe_steps_recipe_id", "recipe_steps", ["recipe_id"])


def downgrade():
    op.drop_index("ix_recipe_steps_recipe_id", table_name="recipe_steps")
    op.drop_table("recipe_steps")

    op.drop_index("ix_ingredients_name", table_name="ingredients")
    op.drop_index("ix_ingredients_recipe_id", table_name="ingredients")
    op.drop_table("ingredients")

    op.drop_index("ix_recipes_user_id", table_name="recipes")
    op.drop_table("recipes")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")