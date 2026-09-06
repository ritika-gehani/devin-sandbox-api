from flask import Blueprint, current_app, jsonify, request

from app.store import InvalidItemName, ItemNotFound

bp = Blueprint("items", __name__)

_BOOL_VALUES = {"true": True, "false": False}


class InvalidQueryParam(ValueError):
    pass


def _parse_bool(name: str, raw: str) -> bool:
    try:
        return _BOOL_VALUES[raw.strip().lower()]
    except KeyError:
        raise InvalidQueryParam(f"{name} must be 'true' or 'false'") from None


@bp.errorhandler(ItemNotFound)
def handle_item_not_found(_exc: ItemNotFound):
    return jsonify(error="item not found"), 404


@bp.errorhandler(InvalidItemName)
def handle_invalid_item_name(exc: InvalidItemName):
    return jsonify(error=str(exc)), 400


@bp.errorhandler(InvalidQueryParam)
def handle_invalid_query_param(exc: InvalidQueryParam):
    return jsonify(error=str(exc)), 400


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
        wanted = _parse_bool("done", done)
        items = [i for i in items if i.done is wanted]
    return jsonify([i.to_dict() for i in items])


@bp.post("/items")
def create_item():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}
    item = store().add(payload.get("name"))
    return jsonify(item.to_dict()), 201


@bp.get("/items/<int:item_id>")
def get_item(item_id: int):
    return jsonify(store().get(item_id).to_dict())


@bp.post("/items/<int:item_id>/done")
def complete_item(item_id: int):
    return jsonify(store().mark_done(item_id).to_dict())


@bp.delete("/items/<int:item_id>")
def delete_item(item_id: int):
    store().remove(item_id)
    return "", 204
