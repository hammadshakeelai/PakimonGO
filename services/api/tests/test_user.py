import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_token_valid"}


def test_get_me_auto_creates_user():
    resp = client.get("/v1/users/me", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["userId"] == "test_user_default"
    assert data["email"] == "test@pakimongo.example"
    assert data["status"] == "active"
    assert data["ageBand"] is None
    assert data["homeRegion"] is None


def test_get_me_requires_auth():
    resp = client.get("/v1/users/me")
    assert resp.status_code == 401


def test_patch_me_updates_profile():
    resp = client.patch("/v1/users/me", json={
        "ageBand": "18-24",
        "homeRegion": "PK-IS",
    }, headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ageBand"] == "18-24"
    assert data["homeRegion"] == "PK-IS"


def test_patch_me_partial_update():
    resp = client.patch("/v1/users/me", json={
        "homeRegion": "PK-PB",
    }, headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["homeRegion"] == "PK-PB"


def test_patch_me_requires_auth():
    resp = client.patch("/v1/users/me", json={"ageBand": "25-34"})
    assert resp.status_code == 401


def test_delete_me_requires_auth():
    resp = client.delete("/v1/users/me")
    assert resp.status_code == 401


def test_delete_me_scrubs_pii_and_deactivates():
    headers = {"Authorization": "Bearer test_user_to_delete"}
    client.get("/v1/users/me", headers=headers)  # auto-create
    client.patch("/v1/users/me", json={
        "ageBand": "18-24",
        "homeRegion": "PK-IS",
    }, headers=headers)

    resp = client.delete("/v1/users/me", headers=headers)
    assert resp.status_code == 204

    me = client.get("/v1/users/me", headers=headers).json()
    assert me["status"] == "deleted"
    assert me["ageBand"] is None
    assert me["homeRegion"] is None


def test_delete_me_is_idempotent():
    headers = {"Authorization": "Bearer test_user_delete_twice"}
    client.get("/v1/users/me", headers=headers)  # auto-create
    first = client.delete("/v1/users/me", headers=headers)
    second = client.delete("/v1/users/me", headers=headers)
    assert first.status_code == 204
    assert second.status_code == 204


def test_deleted_user_excluded_from_search():
    headers = {"Authorization": "Bearer test_user_findme_deleted"}
    client.get("/v1/users/me", headers=headers)  # auto-create
    other_headers = {"Authorization": "Bearer test_user_searcher"}
    before = client.get(
        "/v1/users/search", params={"q": "findme_deleted"}, headers=other_headers
    ).json()
    assert before["total"] == 1

    client.delete("/v1/users/me", headers=headers)

    after = client.get(
        "/v1/users/search", params={"q": "findme_deleted"}, headers=other_headers
    ).json()
    assert after["total"] == 0
