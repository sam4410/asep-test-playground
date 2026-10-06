import routers


def test_routers_package_has_application_docstring():
    assert routers.__doc__ == "Application API routers."


def test_create_todo_returns_created_todo(client):
    response = client.post(
        "/todos",
        json={"title": "  Buy groceries  ", "description": "Milk", "completed": False},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy groceries"
    assert body["description"] == "Milk"
    assert body["completed"] is False
    assert isinstance(body["id"], int)
    assert body["created_at"]


def test_list_todos_returns_todos_in_id_order(client):
    first = client.post("/todos", json={"title": "First"}).json()
    second = client.post("/todos", json={"title": "Second"}).json()

    response = client.get("/todos")

    assert response.status_code == 200
    todos = response.json()
    returned_ids = [todo["id"] for todo in todos]
    assert returned_ids == sorted(returned_ids)
    assert returned_ids[-2:] == [first["id"], second["id"]]


def test_get_todo_returns_todo_and_not_found_error(client):
    created = client.post("/todos", json={"title": "Read"}).json()

    response = client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Read"

    missing = client.get("/todos/999999")

    assert missing.status_code == 404
    assert missing.json() == {"detail": "Todo not found"}


def test_update_todo_updates_only_supplied_fields(client):
    created = client.post(
        "/todos",
        json={"title": "Old title", "description": "Details", "completed": False},
    ).json()

    response = client.put(
        f"/todos/{created['id']}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New title"
    assert body["description"] == "Details"
    assert body["completed"] is True

    missing = client.put("/todos/999999", json={"title": "Unavailable"})

    assert missing.status_code == 404
    assert missing.json() == {"detail": "Todo not found"}


def test_delete_todo_removes_todo_and_handles_missing_id(client):
    created = client.post("/todos", json={"title": "Temporary"}).json()

    response = client.delete(f"/todos/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/todos/{created['id']}").status_code == 404

    missing = client.delete("/todos/999999")

    assert missing.status_code == 404
    assert missing.json() == {"detail": "Todo not found"}