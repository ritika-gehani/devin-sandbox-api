from flask import Blueprint, current_app, jsonify, request

from app.store import ItemNotFound

bp = Blueprint("items", __name__)


@bp.errorhandler(ItemNotFound)
def handle_item_not_found(_exc: ItemNotFound):
    return jsonify(error="item not found"), 404


def store():
    return current_app.config["STORE"]


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/items")
def list_items():
    done = request.args.get("done")
    items = store().list()
    if done is not None:
        items = [i for i in items if i.done == done]
    return jsonify([i.to_dict() for i in items])


@bp.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    item = store().add(payload.get("name"))
    return jsonify(item.to_dict()), 201


@bp.get("/items/<int:item_id>")
def get_item(item_id: int):
    return jsonify(store().get(item_id).to_dict())


@bp.post("/items/<int:item_id>/done")
def complete_item(item_id: int):
    return jsonify(store().mark_done(item_id).to_dict())
