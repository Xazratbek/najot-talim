import pytest

pytestmark = pytest.mark.asyncio


async def test_create_todo(client):
    resp = await client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "Buy milk"
    assert body["done"] is False
    assert "id" in body


async def test_list_todos(client):
    await client.post("/todos", json={"title": "A"})
    await client.post("/todos", json={"title": "B"})

    resp = await client.get("/todos")
    assert resp.status_code == 200
    titles = [t["title"] for t in resp.json()]
    assert titles == ["A", "B"]


async def test_get_todo(client):
    created = (await client.post("/todos", json={"title": "Read book"})).json()

    resp = await client.get(f"/todos/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Read book"


async def test_get_todo_not_found(client):
    resp = await client.get("/todos/999")
    assert resp.status_code == 404


async def test_update_todo(client):
    created = (await client.post("/todos", json={"title": "Old"})).json()

    resp = await client.put(f"/todos/{created['id']}", json={"title": "New", "done": True})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "New"
    assert body["done"] is True


async def test_update_todo_not_found(client):
    resp = await client.put("/todos/999", json={"title": "New"})
    assert resp.status_code == 404


async def test_delete_todo(client):
    created = (await client.post("/todos", json={"title": "Temp"})).json()

    resp = await client.delete(f"/todos/{created['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/todos/{created['id']}")
    assert resp.status_code == 404


async def test_delete_todo_not_found(client):
    resp = await client.delete("/todos/999")
    assert resp.status_code == 404
