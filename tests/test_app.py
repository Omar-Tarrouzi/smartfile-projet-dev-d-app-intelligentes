import pytest

from smartfiles import create_app


@pytest.fixture
def client(tmp_path):
    root = tmp_path / "allowed"
    root.mkdir()
    (root / "notes.TXT").write_text("abc", encoding="utf-8")
    (root / "sub").mkdir()
    (root / "sub" / "photo.jpg").write_bytes(b"12345")
    (root / ".env").write_text("secret", encoding="utf-8")
    (root / ".git").mkdir()
    (root / ".git" / "config").write_text("secret", encoding="utf-8")
    app = create_app({"TESTING": True, "ALLOWED_ROOTS": [str(root)]})
    return app.test_client(), root


def test_dashboard_and_health(client):
    http, _ = client
    assert http.get("/").status_code == 200
    assert http.get("/health").json["status"] == "ok"


def test_recursive_read_only_scan(client):
    http, root = client
    before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    response = http.post("/scan", json={"path": str(root)})
    assert response.status_code == 200
    data = response.json
    assert data["total_files"] == 2
    assert data["total_size_bytes"] == 8
    assert data["categories"]["document"]["count"] == 1
    assert {f["path"] for f in data["files"]} == {"notes.TXT", "sub/photo.jpg"}
    assert before == {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize("payload", [None, [], {}, {"path": 42}, {"path": "relative"}])
def test_invalid_payload(client, payload):
    http, _ = client
    assert http.post("/scan", json=payload).status_code == 400


def test_outside_and_prefix_sibling(client):
    http, root = client
    sibling = root.parent / "allowed-other"
    sibling.mkdir()
    for path in (root.parent, sibling, root / ".."):
        assert http.post("/scan", json={"path": str(path)}).status_code == 403


def test_file_missing_and_excluded(client):
    http, root = client
    assert http.post("/scan", json={"path": str(root / "notes.TXT")}).status_code == 400
    assert http.post("/scan", json={"path": str(root / "missing")}).status_code == 400
    assert http.post("/scan", json={"path": str(root / ".git")}).status_code == 403


def test_limit_and_empty(client):
    http, root = client
    http.application.config["MAX_FILES"] = 1
    data = http.post("/scan", json={"path": str(root)}).json
    assert data["truncated"] and data["total_files"] == 1
    empty = root / "empty"
    empty.mkdir()
    data = http.post("/scan", json={"path": str(empty)}).json
    assert data["total_files"] == 0 and not data["truncated"]


def test_links_are_not_followed(client):
    http, root = client
    link = root / "linked"
    try:
        link.symlink_to(root.parent, target_is_directory=True)
    except OSError:
        pytest.skip("La création de liens nécessite un droit Windows spécifique.")
    assert http.post("/scan", json={"path": str(link)}).status_code == 403
    assert http.post("/scan", json={"path": str(root)}).json["total_files"] == 2


def test_no_mutating_endpoints(client):
    http, _ = client
    for route in ("/clean", "/rename", "/organize", "/undo", "/prompt"):
        assert http.post(route, json={}).status_code == 404
