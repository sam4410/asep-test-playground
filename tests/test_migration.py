import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest
import sqlalchemy as sa


MIGRATION_PATH = (
    Path(__file__).parents[1]
    / "alembic"
    / "versions"
    / "81bd664a1450_auto_migration.py"
)
SPEC = importlib.util.spec_from_file_location("todo_migration", MIGRATION_PATH)
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


def test_upgrade_creates_todos_table_and_id_index():
    with patch.object(migration.op, "create_table") as create_table, patch.object(
        migration.op,
        "create_index",
    ) as create_index:
        migration.upgrade()

    create_table.assert_called_once()
    table_args = create_table.call_args.args
    assert table_args[0] == "todos"

    columns = {
        item.name: item
        for item in table_args[1:]
        if isinstance(item, sa.Column)
    }
    assert set(columns) == {
        "id",
        "title",
        "description",
        "completed",
        "created_at",
    }
    assert isinstance(columns["id"].type, sa.Integer)
    assert isinstance(columns["title"].type, sa.String)
    assert isinstance(columns["description"].type, sa.String)
    assert isinstance(columns["completed"].type, sa.Boolean)
    assert isinstance(columns["created_at"].type, sa.DateTime)
    assert not columns["id"].nullable
    assert not columns["title"].nullable
    assert columns["description"].nullable
    assert not columns["completed"].nullable
    assert not columns["created_at"].nullable

    create_index.assert_called_once_with(
        "ix_todos_id",
        "todos",
        ["id"],
        unique=False,
    )


def test_upgrade_propagates_table_creation_errors():
    with patch.object(
        migration.op,
        "create_table",
        side_effect=RuntimeError("cannot create table"),
    ):
        with pytest.raises(RuntimeError, match="cannot create table"):
            migration.upgrade()


def test_downgrade_drops_index_before_table():
    with patch.object(migration.op, "drop_index") as drop_index, patch.object(
        migration.op,
        "drop_table",
    ) as drop_table:
        migration.downgrade()

    assert drop_index.call_args_list[0].args == ("ix_todos_id",)
    assert drop_index.call_args.kwargs == {"table_name": "todos"}
    drop_table.assert_called_once_with("todos")
    assert drop_index.call_count == 1
    assert drop_table.call_count == 1


def test_downgrade_propagates_index_drop_errors():
    with patch.object(
        migration.op,
        "drop_index",
        side_effect=RuntimeError("cannot drop index"),
    ), patch.object(migration.op, "drop_table") as drop_table:
        with pytest.raises(RuntimeError, match="cannot drop index"):
            migration.downgrade()

    drop_table.assert_not_called()
