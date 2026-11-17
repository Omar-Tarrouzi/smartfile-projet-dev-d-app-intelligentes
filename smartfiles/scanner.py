"""Scanner de métadonnées en lecture seule ; aucun contenu n'est chargé."""

import os
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from .safety import IGNORED, is_link

CATEGORIES = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic"},
    "document": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "presentation": {".ppt", ".pptx", ".odp"},
    "tableur": {".xls", ".xlsx", ".csv", ".ods"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".ogg"},
    "archive": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp"},
    "temporaire": {".tmp", ".log", ".bak", ".swp", ".cache"},
}


def analyze(folder: Path, max_files=10000):
    files, warnings = [], []
    categories = defaultdict(lambda: {"count": 0, "size_bytes": 0})
    truncated = False

    def on_error(error):
        if len(warnings) < 100:
            warnings.append(f"Dossier inaccessible : {error.filename}")

    for base, dirs, names in os.walk(folder, followlinks=False, onerror=on_error):
        safe_dirs = []
        for name in sorted(dirs):
            try:
                if (
                    name not in IGNORED
                    and not name.startswith(".")
                    and not is_link(Path(base) / name)
                ):
                    safe_dirs.append(name)
            except OSError as error:
                on_error(error)
        dirs[:] = safe_dirs
        for name in sorted(names):
            if name.startswith("."):
                continue
            path = Path(base) / name
            try:
                if is_link(path) or not path.is_file():
                    continue
                if len(files) >= max_files:
                    truncated = True
                    break
                info = path.stat()
                extension = path.suffix.lower()
                category = next((k for k, v in CATEGORIES.items() if extension in v), "autre")
                files.append(
                    {
                        "path": path.relative_to(folder).as_posix(),
                        "name": name,
                        "extension": extension,
                        "size_bytes": info.st_size,
                        "category": category,
                        "modified_at": datetime.fromtimestamp(info.st_mtime, UTC).isoformat(),
                        "accessed_at": datetime.fromtimestamp(info.st_atime, UTC).isoformat(),
                    }
                )
                categories[category]["count"] += 1
                categories[category]["size_bytes"] += info.st_size
            except OSError as error:
                on_error(error)
        if truncated:
            break
    return {
        "folder": str(folder),
        "total_files": len(files),
        "total_size_bytes": sum(f["size_bytes"] for f in files),
        "categories": dict(categories),
        "files": files,
        "warnings": warnings,
        "truncated": truncated,
    }
