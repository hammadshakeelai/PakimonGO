import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_token_valid"}


def test_default_version_is_v1():
    """No Accept-Version header defaults to v1."""
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.headers.get("api-version") == "v1"


def test_accept_version_v1():
    """Explicit v1 version accepted."""
    response = client.get("/health/live", headers={"Accept-Version": "v1"})
    assert response.status_code == 200
    assert response.headers.get("api-version") == "v1"


def test_accept_version_v2():
    """Explicit v2 version accepted."""
    response = client.get("/health/live", headers={"Accept-Version": "v2"})
    assert response.status_code == 200
    assert response.headers.get("api-version") == "v2"


def test_invalid_version_defaults_to_v1():
    """Invalid version defaults to v1."""
    response = client.get("/health/live", headers={"Accept-Version": "v99"})
    assert response.status_code == 200
    assert response.headers.get("api-version") == "v1"


def test_version_header_on_protected_endpoint():
    """Version header works on protected endpoints."""
    response = client.get("/v1/users/me", headers=AUTH_HEADER)
    assert response.status_code == 200
    assert response.headers.get("api-version") == "v1"


def test_health_endpoints_are_public():
    """Health endpoints require no auth."""
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200
