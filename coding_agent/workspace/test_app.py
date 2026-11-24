import pytest
from fastapi.testclient import TestClient
from app import app, todos


@pytest.fixture(autouse=True)
def reset_data():
    todos.clear()
    yield
    todos.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_todo_defaults(client):
    response = client.post("/todos", json={"title": "Test Todo"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Todo"
    assert data["description"] == ""
    assert data["completed"] is False


def test_create_todo_with_all_fields(client):
    payload = {
        "title": "Grocery Shopping",
        "description": "Buy milk and eggs",
        "completed": True,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Grocery Shopping"
    assert data["description"] == "Buy milk and eggs"
    assert data["completed"] is True


def test_list_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_populated(client):
    client.post("/todos", json={"title": "Todo 1"})
    client.post("/todos", json={"title": "Todo 2"})

    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


def test_get_todo_by_id_success(client):
    create_res = client.post("/todos", json={"title": "Find Me", "description": "Details"})
    todo_id = create_res.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Find Me"
    assert data["description"] == "Details"


def test_get_todo_by_id_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo_success(client):
    create_res = client.post("/todos", json={"title": "Old Title", "completed": False})
    todo_id = create_res.json()["id"]

    update_payload = {"title": "New Title", "completed": True}
    response = client.put(f"/todos/{todo_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "New Title"
    assert data["completed"] is True

    # Confirm update via GET
    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.json()["title"] == "New Title"
    assert get_res.json()["completed"] is True


def test_update_todo_partial(client):
    create_res = client.post(
        "/todos", json={"title": "Title", "description": "Original Desc", "completed": False}
    )
    todo_id = create_res.json()["id"]

    response = client.patch(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title"
    assert data["description"] == "Original Desc"
    assert data["completed"] is True


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"title": "Does Not Exist"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo_success(client):
    create_res = client.post("/todos", json={"title": "Delete Me"})
    todo_id = create_res.json()["id"]

    del_res = client.delete(f"/todos/{todo_id}")
    assert del_res.status_code == 200

    # Ensure it's deleted
    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.status_code == 404

    # Ensure list is empty
    list_res = client.get("/todos")
    assert list_res.json() == []


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_data_reset_between_tests(client):
    # This test verifies that the reset_data fixture prevents state leakage
    assert len(todos) == 0
    client.post("/todos", json={"title": "Isolated Todo"})
    assert len(todos) == 1
