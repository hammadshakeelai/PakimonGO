import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.infrastructure.queue.queue import get_queue
from src.infrastructure.worker.scoring_worker import process_pending_jobs
from src.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_token_valid"}


def _process_pending():
    process_pending_jobs(get_queue())


def _create_upload(sha_suffix: str = "a"):
    sha = sha_suffix * 64
    resp = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": sha,
    }, headers=AUTH_HEADER)
    return resp.json()["mediaAssetId"]


def test_create_wild_submission():
    media_asset_id = _create_upload("1")
    response = client.post("/v1/submissions", json={
        "mediaAssetId": media_asset_id,
        "animalContext": "wild",
        "realName": "House Sparrow",
        "cuteName": "Tiny Captain",
        "caption": "Resting near the garden path.",
        "tags": ["sparrow", "garden", "morning"],
        "visibility": "private",
        "foregroundLocation": {
            "latitude": 33.6844,
            "longitude": 73.0479,
            "accuracyMeters": 18.5,
        },
    }, headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    sub_id = data["submissionId"]
    assert sub_id.startswith("sub_")
    assert data["scoreState"]["status"] == "ai_evaluated"
    assert data["scoreState"]["visiblePoints"] is None

    _process_pending()

    get_resp = client.get(f"/v1/submissions/{sub_id}", headers=AUTH_HEADER)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["scoreState"]["status"] == "scored"
    assert data["scoreState"]["visiblePoints"] == 25
    assert data["scoreState"]["explanationSummary"] == "normal"
    assert data["visibility"] == "private"
    assert "publicLocation" in data


def test_create_zoo_submission():
    media_asset_id = _create_upload("2")
    response = client.post("/v1/submissions", json={
        "mediaAssetId": media_asset_id,
        "animalContext": "zoo",
        "realName": "Peacock",
        "cuteName": "Feather King",
        "caption": "At the aviary",
        "tags": ["peacock", "zoo"],
    }, headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert data["scoreState"]["status"] == "capped"
    assert data["scoreState"]["visiblePoints"] == 1
    assert data["scoreState"]["explanationSummary"] == "zoo_cap"


def test_submission_response_no_exact_coords():
    media_asset_id = _create_upload("3")
    response = client.post("/v1/submissions", json={
        "mediaAssetId": media_asset_id,
        "animalContext": "wild",
        "realName": "House Sparrow",
        "cuteName": "Tiny Captain",
        "caption": "Test",
        "tags": [],
    }, headers=AUTH_HEADER)
    data = response.json()
    assert "latitude" not in data
    assert "longitude" not in data
    assert "privateLatitude" not in data
    assert "lat" not in data
    assert "lng" not in data
    assert "deviceId" not in data
    assert "ipAddress" not in data


def test_get_submission():
    media_asset_id = _create_upload("4")
    create_resp = client.post("/v1/submissions", json={
        "mediaAssetId": media_asset_id,
        "animalContext": "zoo",
        "realName": "Peacock",
        "cuteName": "Feather King",
        "caption": "At the aviary",
        "tags": ["peacock", "zoo"],
    }, headers=AUTH_HEADER)
    sub_id = create_resp.json()["submissionId"]

    get_resp = client.get(f"/v1/submissions/{sub_id}", headers=AUTH_HEADER)
    assert get_resp.status_code == 200
    assert get_resp.json()["submissionId"] == sub_id


def test_get_submission_not_found():
    response = client.get("/v1/submissions/sub_nonexistent", headers=AUTH_HEADER)
    assert response.status_code == 404


def test_create_submission_missing_media_id():
    response = client.post("/v1/submissions", json={
        "animalContext": "wild",
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_duplicate_submission_capped():
    asset1 = _create_upload("dup")
    first = client.post("/v1/submissions", json={
        "mediaAssetId": asset1,
        "animalContext": "wild",
        "realName": "Sparrow",
        "cuteName": "Tiny",
        "caption": "First",
        "tags": [],
    }, headers=AUTH_HEADER)
    assert first.status_code == 200
    assert first.json()["scoreState"]["status"] == "ai_evaluated"
    sub1_id = first.json()["submissionId"]

    _process_pending()

    get1 = client.get(f"/v1/submissions/{sub1_id}", headers=AUTH_HEADER)
    assert get1.json()["scoreState"]["status"] == "scored"
    assert get1.json()["scoreState"]["visiblePoints"] == 25

    asset2 = _create_upload("dup")
    second = client.post("/v1/submissions", json={
        "mediaAssetId": asset2,
        "animalContext": "wild",
        "realName": "Sparrow",
        "cuteName": "Tiny",
        "caption": "Second (duplicate)",
        "tags": [],
    }, headers=AUTH_HEADER)
    assert second.status_code == 200
    assert second.json()["scoreState"]["status"] == "capped"
    assert second.json()["scoreState"]["visiblePoints"] == 0
    assert second.json()["scoreState"]["explanationSummary"] == "duplicate_cap"
