"""Fabrique de l'application, sans scan lors de l'import."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    demo = Path(__file__).resolve().parent.parent / "demo"
    roots = json.loads(os.getenv("SMARTFILES_ALLOWED_ROOTS", "[]"))
    if not isinstance(roots, list) or any(not isinstance(p, str) for p in roots):
        raise ValueError("SMARTFILES_ALLOWED_ROOTS doit être une liste JSON de chemins.")
    app.config.from_mapping(
        ALLOWED_ROOTS=roots or [str(demo)],
        MAX_FILES=int(os.getenv("SMARTFILES_MAX_FILES", "10000")),
        MAX_CONTENT_LENGTH=16 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    if app.config["MAX_FILES"] < 1:
        raise ValueError("MAX_FILES doit être positif.")
    from .routes import bp

    app.register_blueprint(bp)
    return app
