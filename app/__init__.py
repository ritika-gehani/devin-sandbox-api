from flask import Flask

from app.store import ItemStore
from app.routes import bp


def create_app(store: ItemStore | None = None) -> Flask:
    app = Flask(__name__)
    app.config["STORE"] = store or ItemStore()
    app.register_blueprint(bp)
    return app
