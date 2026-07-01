import os
import sys
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.infrastructure.database.repositories import (
    create_media_asset,
    create_submission,
    create_score_event,
    get_or_create_user,
    update_submission_status,
)
from src.infrastructure.database.session import get_db
from src.main import app

client = TestClient(app)
AUTH_DEFAULT = {"Authorization": "Bearer test_token_valid"}
AUTH2 = {"Authorization": "Bearer test_user_user2"}

_DEFAULT_USER = "test_user_default"


def _seed(user_id: str, species: str, context: str, points: int, status: str = "scored"):
    db = next(get_db())
    try:
        get_or_create_user(db, user_id)
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
        db.close()
    finally:
        db.close()


def test_collection_returns_species():
    _seed(_DEFAULT_USER, "Aquila chrysaetos", "wild", 25)
    _seed(_DEFAULT_USER, "Panthera leo", "zoo", 1)
    resp = client.get("/v1/users/me/collection", headers=AUTH_DEFAULT)
    assert resp.status_code == 200
    data = resp.json()
    assert data["userId"] == _DEFAULT_USER
    assert len(data["species"]) >= 2


def test_collection_empty_for_new_user():
    resp = client.get("/v1/users/me/collection", headers=AUTH2)
    assert resp.status_code == 200
    assert resp.json()["species"] == []


def test_collection_requires_auth():
    resp = client.get("/v1/users/me/collection")
    assert resp.status_code == 401


def test_leaderboard_returns_entries():
    _seed(_DEFAULT_USER, "Canis lupus", "wild", 25)
    resp = client.get("/v1/leaderboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "entries" in data
    assert data["totalReturned"] > 0
    top = data["entries"][0]
    assert "userId" in top
    assert "totalScore" in top
    assert top["totalScore"] >= 25


def test_leaderboard_public_no_auth_required():
    resp = client.get("/v1/leaderboard")
    assert resp.status_code == 200


def test_leaderboard_respects_limit():
    resp = client.get("/v1/leaderboard?limit=1")
    assert resp.status_code == 200
    assert len(resp.json()["entries"]) <= 1


def test_leaderboard_invalid_limit():
    assert client.get("/v1/leaderboard?limit=0").status_code == 422
    assert client.get("/v1/leaderboard?limit=501").status_code == 422
