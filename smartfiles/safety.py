"""Validation des racines et exclusion des liens / jonctions."""

import stat
from pathlib import Path

IGNORED = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".smartfiles_trash",
    ".pytest_cache",
}


def is_link(path):
    info = path.lstat()
    return path.is_symlink() or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def allowed_folder(raw, roots):
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("Un chemin de dossier est requis.")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise ValueError("Utilisez un chemin absolu.")
    for part in [path, *path.parents]:
        if is_link(part):
            raise PermissionError("Les liens et jonctions ne sont pas autorisés.")
    path = path.resolve(strict=True)
    if not path.is_dir():
        raise ValueError("Le chemin doit désigner un dossier.")
    authorized = [Path(p).expanduser().resolve(strict=True) for p in roots]
    if not any(path.is_relative_to(p) for p in authorized):
        raise PermissionError("Ce dossier est hors des racines autorisées.")
    if any(p in IGNORED for p in path.parts):
        raise PermissionError("Ce dossier est exclu de l'analyse.")
    return path
