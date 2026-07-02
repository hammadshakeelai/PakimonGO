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
