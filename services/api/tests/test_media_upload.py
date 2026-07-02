import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_token_valid"}

SAMPLE_SHA = "a" * 64
BIG_SHA = "b" * 64


def test_create_upload_intent():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "mediaAssetId" in data
    assert data["mediaAssetId"].startswith("media_")
    assert "uploadUrl" in data
    assert "expiresAt" in data


def test_create_upload_intent_missing_fields():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_create_upload_intent_oversized():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 50 * 1024 * 1024,
        "sha256": BIG_SHA,
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_create_upload_intent_bad_content_type():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.gif",
        "contentType": "image/gif",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_complete_upload():
    create_resp = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    media_asset_id = create_resp.json()["mediaAssetId"]

    response = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_complete_upload_wrong_sha():
    create_resp = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    media_asset_id = create_resp.json()["mediaAssetId"]

    response = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": "b" * 64,
    }, headers=AUTH_HEADER)
    assert response.status_code == 404


def test_complete_upload_missing():
    response = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": "media_nonexistent",
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    assert response.status_code == 404


def test_complete_upload_missing_sha():
    response = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": "media_001",
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_privacy_no_exact_location_in_response():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    data = response.json()
    assert "latitude" not in data
    assert "longitude" not in data
    assert "deviceId" not in data
    assert "ipAddress" not in data


def test_upload_intent_requires_auth():
    response = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    })
    assert response.status_code == 401


def test_upload_file_roundtrip():
    create_resp = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    media_asset_id = create_resp.json()["mediaAssetId"]

    upload_resp = client.put(
        f"/v1/media/upload/{media_asset_id}",
        files={"file": ("test.jpg", b"fake-image-bytes", "image/jpeg")},
        headers=AUTH_HEADER,
    )
    assert upload_resp.status_code == 200
    assert upload_resp.json()["status"] == "ok"

    complete_resp = client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_asset_id,
        "sha256": SAMPLE_SHA,
    }, headers=AUTH_HEADER)
    assert complete_resp.status_code == 200
    assert complete_resp.json()["status"] == "ok"
