"""Adaptateurs HTTP : validation, appel métier, réponse JSON."""

from flask import Blueprint, current_app, jsonify, render_template, request

from .safety import allowed_folder
from .scanner import analyze

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html", roots=current_app.config["ALLOWED_ROOTS"])


@bp.get("/health")
def health():
    return jsonify(status="ok", version="0.1.0")


@bp.post("/scan")
def scan():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Un objet JSON est requis."), 400
    try:
        folder = allowed_folder(data.get("path"), current_app.config["ALLOWED_ROOTS"])
        return jsonify(analyze(folder, current_app.config["MAX_FILES"]))
    except PermissionError:
        return jsonify(error="Accès refusé : dossier non autorisé ou inaccessible."), 403
    except (ValueError, FileNotFoundError, NotADirectoryError):
        return jsonify(error="Chemin invalide : utilisez un dossier absolu existant."), 400
    except OSError:
        return jsonify(error="Impossible de lire ce dossier."), 400
