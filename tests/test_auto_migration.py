import importlib
from unittest.mock import call
from unittest.mock import Mock

import sqlalchemy as sa


migration = importlib.import_module(
    "migrations.versions.d2bf9fb5b85f_auto_migration"
)


def test_upgrade_creates_todo_schema_indexes_and_trigger(monkeypatch):
    create_table = Mock()
    create_index = Mock()
    execute = Mock()
    monkeypatch.setattr(migration.op, "create_table", create_table)
    monkeypatch.setattr(migration.op, "create_index", create_index)
    monkeypatch.setattr(migration.op, "execute", execute)

    migration.upgrade()

    create_table.assert_called_once()
    table_args = create_table.call_args.args
    assert table_args[0] == "todos"
    columns = [item for item in table_args[1:] if isinstance(item, sa.Column)]
    assert [column.name for column in columns] == [
        "id",
        "title",
        "completed",
        "created_at",
        "updated_at",
    ]
    assert isinstance(columns[0].type, sa.Integer)
    assert isinstance(columns[0].identity, sa.Identity)
    assert columns[0].nullable is False
    assert isinstance(columns[1].type, sa.String)
    assert columns[1].type.length == 500
    assert columns[1].nullable is False
    assert columns[2].nullable is False
    assert str(columns[2].server_default.arg) == "false"
    assert columns[3].nullable is False
    assert str(columns[3].server_default.arg) == "CURRENT_TIMESTAMP"
    assert columns[4].nullable is False
    assert str(columns[4].server_default.arg) == "CURRENT_TIMESTAMP"

    constraints = [
        item
        for item in table_args[1:]
        if isinstance(item, sa.Constraint)
    ]
    check_constraints = [
        item
        for item in constraints
        if isinstance(item, sa.CheckConstraint)
    ]
    assert len(check_constraints) == 1
    assert check_constraints[0].name == "ck_todos_title_not_blank"
    assert str(check_constraints[0].sqltext) == "length(btrim(title)) > 0"
    assert any(isinstance(item, sa.PrimaryKeyConstraint) for item in constraints)

    assert create_index.call_args_list == [
        call("ix_todos_created_at", "todos", ["created_at"]),
        call(
            "ix_todos_completed_created_at",
            "todos",
            ["completed", "created_at"],
        ),
    ]
    assert execute.call_args_list == [
        call(
            "CREATE OR REPLACE FUNCTION set_todos_updated_at() "
            "RETURNS TRIGGER LANGUAGE plpgsql AS $$ "
            "BEGIN NEW.updated_at = CURRENT_TIMESTAMP; "
            "RETURN NEW; END; $$"
        ),
        call(
            "CREATE TRIGGER todos_updated_at "
            "BEFORE UPDATE ON todos FOR EACH ROW "
            "EXECUTE FUNCTION set_todos_updated_at()"
        ),
    ]


def test_downgrade_removes_trigger_function_indexes_and_table(monkeypatch):
    execute = Mock()
    drop_index = Mock()
    drop_table = Mock()
    monkeypatch.setattr(migration.op, "execute", execute)
    monkeypatch.setattr(migration.op, "drop_index", drop_index)
    monkeypatch.setattr(migration.op, "drop_table", drop_table)

    migration.downgrade()

    assert execute.call_args_list == [
        call("DROP TRIGGER IF EXISTS todos_updated_at ON todos"),
        call("DROP FUNCTION IF EXISTS set_todos_updated_at()"),
    ]
    assert drop_index.call_args_list == [
        call("ix_todos_completed_created_at", table_name="todos"),
        call("ix_todos_created_at", table_name="todos"),
    ]
    drop_table.assert_called_once_with("todos")


def test_migration_identifiers_are_root_revision_metadata():
    assert migration.revision == "d2bf9fb5b85f"
    assert migration.down_revision is None
    assert migration.branch_labels is None
    assert migration.depends_on is None