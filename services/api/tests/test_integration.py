import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.infrastructure.queue.queue import get_queue
from src.infrastructure.worker.scoring_worker import process_pending_jobs
from src.main import app

client = TestClient(app)
AUTH = {"Authorization": "Bearer test_token_valid"}
AUTH2 = {"Authorization": "Bearer test_user_user2"}


def _process_pending():
    process_pending_jobs(get_queue())


def _ensure_user(auth):
    """GET /users/me to auto-create the User row for leaderboard/collection joins."""
    client.get("/v1/users/me", headers=auth)


def _full_upload_flow(sha_suffix: str):
    sha = sha_suffix * 64
    intent = client.post("/v1/media/upload-intent", json={
        "fileName": "sparrow.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": sha,
    }, headers=AUTH)
    media_id = intent.json()["mediaAssetId"]

    client.put(
        f"/v1/media/upload/{media_id}",
        files={"file": ("test.jpg", b"fake-image-bytes", "image/jpeg")},
        headers=AUTH,
    )

    client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_id,
        "sha256": sha,
    }, headers=AUTH)
    return media_id


def _create_submission(media_id, context, species, auth=AUTH, **overrides):
    body = {
        "mediaAssetId": media_id,
        "animalContext": context,
        "realName": species,
        "cuteName": f"cute_{species}",
        "caption": f"A {species}",
        "tags": [context, species],
        "visibility": "private",
        "foregroundLocation": {
            "latitude": 33.6844,
            "longitude": 73.0479,
            "accuracyMeters": 18.5,
        },
    }
    body.update(overrides)
    return client.post("/v1/submissions", json=body, headers=auth)


def test_end_to_end_wild_capture():
    _ensure_user(AUTH)
    media_id = _full_upload_flow("inte")
    sub_resp = _create_submission(media_id, "wild", "Passer domesticus")
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    sub_id = sub_data["submissionId"]
    assert sub_id.startswith("sub_")
    assert sub_data["scoreState"]["status"] == "ai_evaluated"

    _process_pending()

    get_resp = client.get(f"/v1/submissions/{sub_id}", headers=AUTH)
    assert get_resp.status_code == 200
    assert get_resp.json()["scoreState"]["status"] == "scored"
    assert get_resp.json()["scoreState"]["visiblePoints"] == 25

    coll_resp = client.get("/v1/users/me/collection", headers=AUTH)
    assert coll_resp.status_code == 200
    coll_data = coll_resp.json()
    assert coll_data["userId"] == "test_user_default"
    species_names = [s["species"] for s in coll_data["species"]]
    assert "Passer domesticus" in species_names

    lb_resp = client.get("/v1/leaderboard")
    assert lb_resp.status_code == 200
    lb_data = lb_resp.json()
    entries = lb_data["entries"]
    user_entry = next((e for e in entries if e["userId"] == "test_user_default"), None)
    assert user_entry is not None
    assert user_entry["totalScore"] >= 25


def test_end_to_end_zoo_capture():
    media_id = _full_upload_flow("inte2")
    sub_resp = _create_submission(media_id, "zoo", "Pavo cristatus")
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    assert sub_data["scoreState"]["status"] == "capped"
    assert sub_data["scoreState"]["visiblePoints"] == 1
    assert sub_data["scoreState"]["explanationSummary"] == "zoo_cap"


def test_end_to_end_duplicate_detection():
    media_id1 = _full_upload_flow("intedup")
    sub1 = _create_submission(media_id1, "wild", "Columba livia")
    assert sub1.status_code == 200
    sub1_data = sub1.json()
    assert sub1_data["scoreState"]["status"] == "ai_evaluated"

    _process_pending()

    get1 = client.get(f"/v1/submissions/{sub1_data['submissionId']}", headers=AUTH)
    assert get1.json()["scoreState"]["visiblePoints"] == 25

    media_id2 = _full_upload_flow("intedup")
    sub2 = _create_submission(media_id2, "wild", "Columba livia")
    assert sub2.status_code == 200
    assert sub2.json()["scoreState"]["visiblePoints"] == 0
    assert sub2.json()["scoreState"]["explanationSummary"] == "duplicate_cap"


def test_end_to_end_multiuser_collection():
    _ensure_user(AUTH)
    _ensure_user(AUTH2)
    media_a1 = _full_upload_flow("multe")
    media_a2 = _full_upload_flow("multe2")
    _create_submission(media_a1, "wild", "Felis catus")
    _create_submission(media_a2, "zoo", "Panthera leo")
    _process_pending()

    coll_a = client.get("/v1/users/me/collection", headers=AUTH)
    assert coll_a.status_code == 200
    coll_a_names = [s["species"] for s in coll_a.json()["species"]]
    assert "Felis catus" in coll_a_names
    assert "Panthera leo" in coll_a_names

    _full_upload_flow("multf1")
    intent_b = client.post("/v1/media/upload-intent", json={
        "fileName": "eagle.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": "multf1" * 16 + "bb",
    }, headers=AUTH2)
    media_b_id = intent_b.json()["mediaAssetId"]
    client.put(
        f"/v1/media/upload/{media_b_id}",
        files={"file": ("eagle.jpg", b"eagle-img", "image/jpeg")},
        headers=AUTH2,
    )
    client.post("/v1/media/complete-upload", json={
        "mediaAssetId": media_b_id,
        "sha256": "multf1" * 16 + "bb",
    }, headers=AUTH2)
    _create_submission(media_b_id, "wild", "Aquila chrysaetos", auth=AUTH2)
    _process_pending()

    coll_b = client.get("/v1/users/me/collection", headers=AUTH2)
    assert coll_b.status_code == 200
    coll_b_names = [s["species"] for s in coll_b.json()["species"]]
    assert "Felis catus" not in coll_b_names
    assert "Aquila chrysaetos" in coll_b_names

    lb = client.get("/v1/leaderboard")
    assert lb.status_code == 200
    entries = lb.json()["entries"]
    user_ids = [e["userId"] for e in entries]
    assert "test_user_default" in user_ids
    assert "user2" in user_ids


def test_end_to_end_submission_list():
    _ensure_user(AUTH)
    media_id = _full_upload_flow("intel")
    _create_submission(media_id, "wild", "Strix aluco")
    _process_pending()

    list_resp = client.get("/v1/submissions", headers=AUTH)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert "submissions" in data
    assert "pagination" in data
    sub_ids = [s["submissionId"] for s in data["submissions"]]
    assert len(sub_ids) >= 1

    filtered = client.get("/v1/submissions?status=scored", headers=AUTH)
    assert filtered.status_code == 200
    for s in filtered.json()["submissions"]:
        assert s["status"] == "scored"
        assert s["scoreEvent"] is not None


def test_end_to_end_health():
    live = client.get("/health/live")
    assert live.status_code == 200
    assert live.json()["status"] == "ok"

    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ok"
