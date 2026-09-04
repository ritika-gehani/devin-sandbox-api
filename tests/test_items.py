import pytest

from app import create_app
from app.store import (
    MAX_NAME_LENGTH,
    InvalidItemName,
    ItemNotFound,
    ItemStore,
)


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_create_and_list(client):
    res = client.post("/items", json={"name": "buy milk"})
    assert res.status_code == 201
    assert res.get_json()["name"] == "buy milk"

    res = client.get("/items")
    assert [i["name"] for i in res.get_json()] == ["buy milk"]


def test_get_item(client):
    created = client.post("/items", json={"name": "read"}).get_json()
    res = client.get(f"/items/{created['id']}")
    assert res.status_code == 200
    assert res.get_json() == created


def test_mark_done(client):
    created = client.post("/items", json={"name": "ship"}).get_json()
    res = client.post(f"/items/{created['id']}/done")
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_get_unknown_item_returns_404(client):
    res = client.get("/items/999")
    assert res.status_code == 404
    assert res.get_json() == {"error": "item not found"}


def test_mark_done_unknown_item_returns_404(client):
    res = client.post("/items/999/done")
    assert res.status_code == 404
    assert res.get_json() == {"error": "item not found"}
    assert client.get("/items").get_json() == []


def test_store_get_unknown_raises_item_not_found():
    with pytest.raises(ItemNotFound):
        ItemStore().get(999)


@pytest.mark.parametrize(
    "payload",
    [{}, {"name": None}, {"name": ""}, {"name": "   "}, {"name": 42}],
)
def test_create_rejects_missing_or_empty_name(client, payload):
    res = client.post("/items", json=payload)
    assert res.status_code == 400
    assert res.get_json() == {
        "error": "name is required and must be a non-empty string"
    }
    assert client.get("/items").get_json() == []


def test_create_rejects_name_over_max_length(client):
    res = client.post("/items", json={"name": "x" * (MAX_NAME_LENGTH + 1)})
    assert res.status_code == 400
    assert res.get_json() == {
        "error": f"name must be at most {MAX_NAME_LENGTH} characters"
    }
    assert client.get("/items").get_json() == []


def test_create_accepts_name_at_max_length(client):
    res = client.post("/items", json={"name": "x" * MAX_NAME_LENGTH})
    assert res.status_code == 201
    assert res.get_json()["name"] == "x" * MAX_NAME_LENGTH


def test_create_strips_surrounding_whitespace(client):
    res = client.post("/items", json={"name": "  buy milk  "})
    assert res.status_code == 201
    assert res.get_json()["name"] == "buy milk"


def test_rejected_create_does_not_consume_an_id(client):
    client.post("/items", json={"name": ""})
    created = client.post("/items", json={"name": "first"}).get_json()
    assert created["id"] == 1


@pytest.mark.parametrize("name", [None, "", "  ", 42, "x" * (MAX_NAME_LENGTH + 1)])
def test_store_add_rejects_invalid_names(name):
    with pytest.raises(InvalidItemName):
        ItemStore().add(name)
