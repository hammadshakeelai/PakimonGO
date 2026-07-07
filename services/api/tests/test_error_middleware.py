from __future__ import annotations

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.infrastructure.middleware.error_middleware import ErrorHandlingMiddleware, http_exception_handler


@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_exception_handler(HTTPException, http_exception_handler)

    @app.get("/http-exception")
    def raise_http_exc():
        raise HTTPException(status_code=404, detail="Submission not found")

    @app.get("/value-error")
    def raise_value_error():
        raise ValueError("Invalid species name")

    @app.get("/key-error")
    def raise_key_error():
        d = {}
        _ = d["missing"]
        return {}

    @app.get("/permission-error")
    def raise_permission_error():
        raise PermissionError("Token invalid")

    @app.get("/file-not-found")
    def raise_file_not_found():
        raise FileNotFoundError("media/abc.jpg not found")

    @app.get("/internal-error")
    def raise_internal():
        raise RuntimeError("Unexpected failure")

    @app.get("/ok")
    def ok():
        return {"status": "ok"}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestErrorHandlingMiddleware:
    def test_http_exception_404(self, client):
        resp = client.get("/http-exception")
        assert resp.status_code == 404
        data = resp.json()
        assert data["error"]["code"] == "not_found"
        assert data["error"]["message"] == "Submission not found"

    def test_value_error_400(self, client):
        resp = client.get("/value-error")
        assert resp.status_code == 400
        data = resp.json()
        assert data["error"]["code"] == "bad_request"
        assert data["error"]["message"] == "Invalid species name"

    def test_key_error_400(self, client):
        resp = client.get("/key-error")
        assert resp.status_code == 400
        data = resp.json()
        assert data["error"]["code"] == "bad_request"
        assert "Missing required field: 'missing'" in data["error"]["message"]

    def test_permission_error_403(self, client):
        resp = client.get("/permission-error")
        assert resp.status_code == 403
        data = resp.json()
        assert data["error"]["code"] == "forbidden"
        assert data["error"]["message"] == "Token invalid"

    def test_file_not_found_404(self, client):
        resp = client.get("/file-not-found")
        assert resp.status_code == 404
        data = resp.json()
        assert data["error"]["code"] == "not_found"

    def test_internal_error_500(self, client):
        resp = client.get("/internal-error")
        assert resp.status_code == 500
        data = resp.json()
        assert data["error"]["code"] == "internal_error"
        assert data["error"]["message"] == "An unexpected error occurred. Please try again later."

    def test_ok_passthrough(self, client):
        resp = client.get("/ok")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_error_body_has_details(self, client):
        resp = client.get("/value-error")
        data = resp.json()
        assert "details" in data["error"]
        assert isinstance(data["error"]["details"], dict)
