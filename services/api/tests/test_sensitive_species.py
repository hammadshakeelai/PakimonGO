import os
import sys
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.infrastructure.database.repositories import (
    create_media_asset,
    create_submission,
    create_score_event,
    get_or_create_sensitive_species,
    update_submission_status,
    is_sensitive_species,
)
from src.infrastructure.database.session import get_db
from src.main import app

client = TestClient(app)
AUTH_DEFAULT = {"Authorization": "Bearer test_token_valid"}
_DEFAULT_USER = "test_user_default"


def _seed(db, user_id: str, species: str, context: str, points: int, status: str = "scored"):
    asset = create_media_asset(
        db, f"{species}.jpg", "image/jpeg", 1024,
        f"sha256_{uuid.uuid4().hex[:16]}",
        owner_user_id=user_id,
    )
    asset.processing_state = "ready"
    db.commit()
    sub, attr = create_submission(
        db=db, media_asset_id=asset.id, animal_context=context,
        real_name=species, cute_name=f"cute_{species}",
        caption=f"A {species}", tags=[context], user_id=user_id,
    )
    update_submission_status(db, sub.id, status)
    create_score_event(
        db=db, submission_id=sub.id, user_id=user_id, ledger=context,
        points=points, event_type=status, formula_version="1.0",
        explanation_category="species_match" if status == "scored" else "context_cap",
        previous_state="ai_evaluated", new_state=status,
    )
    return sub, attr


def test_sensitive_species_detection():
    db = next(get_db())
    try:
        get_or_create_sensitive_species(db, "Panthera tigris", "Tiger", "coarse_cell", "Endangered")
        assert is_sensitive_species(db, "Panthera tigris") is True
        assert is_sensitive_species(db, "Panthera TIGRIS") is True  # case insensitive
        assert is_sensitive_species(db, "Canis lupus") is False
    finally:
        db.close()


def test_sensitive_species_suppresses_location():
    db = next(get_db())
    try:
        get_or_create_sensitive_species(db, "Panthera tigris", "Tiger", "coarse_cell", "Endangered")
        sub, attr = _seed(db, _DEFAULT_USER, "Panthera tigris", "wild", 25)

        resp = client.get(f"/v1/submissions/{sub.id}", headers=AUTH_DEFAULT)
        assert resp.status_code == 200
        data = resp.json()
        assert data["publicLocation"]["precisionLabel"] == "suppressed"
        assert data["publicLocation"]["suppressedReason"] == "sensitive_species"
        assert data["publicLocation"]["cellId"] == "cell_suppressed"
    finally:
        db.close()


def test_non_sensitive_species_uses_normal_cell():
    db = next(get_db())
    try:
        sub, attr = _seed(db, _DEFAULT_USER, "Canis lupus", "wild", 25)

        resp = client.get(f"/v1/submissions/{sub.id}", headers=AUTH_DEFAULT)
        assert resp.status_code == 200
        data = resp.json()
        assert data["publicLocation"]["precisionLabel"] == "coarse"
        assert "suppressedReason" not in data["publicLocation"]
        assert data["publicLocation"]["cellId"].startswith("cell_")
    finally:
        db.close()


def test_sensitive_species_in_create_response():
    db = next(get_db())
    try:
        get_or_create_sensitive_species(db, "Panthera tigris", "Tiger", "coarse_cell", "Endangered")

        # Create media asset first
        asset = create_media_asset(
            db, "tiger.jpg", "image/jpeg", 1024,
            f"sha256_{uuid.uuid4().hex[:16]}",
            owner_user_id=_DEFAULT_USER,
        )
        asset.processing_state = "ready"
        db.commit()

        # Create submission via API
        resp = client.post("/v1/submissions", json={
            "mediaAssetId": asset.id,
            "animalContext": "wild",
            "realName": "Panthera tigris",
            "cuteName": "Tiger",
            "caption": "A tiger",
            "tags": ["wild"],
        }, headers=AUTH_DEFAULT)
        assert resp.status_code == 200
        data = resp.json()
        assert data["publicLocation"]["precisionLabel"] == "suppressed"
        assert data["publicLocation"]["suppressedReason"] == "sensitive_species"
    finally:
        db.close()
