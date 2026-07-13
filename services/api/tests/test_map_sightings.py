from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import (
    Base,
    CaptureLocation,
    ScoreEvent,
    SensitiveSpecies,
    Submission,
    SubmissionAttribute,
    User,
)
from src.infrastructure.database.session import get_db
from src.main import app

AUTH = {"Authorization": "Bearer test_user_map_alpha"}
ALPHA = "map_alpha"
BETA = "map_beta"


@pytest.fixture
def db_session():
    import tempfile
    from pathlib import Path

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db_path = Path(tmp.name)
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    engine.dispose()
    db_path.unlink(missing_ok=True)


@pytest.fixture
def client(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield TestClient(app)
    app.dependency_overrides.clear()


def _capture(db, user_id, species, lat, lng, visibility="public",
             points=40, status="scored"):
    sub = Submission(user_id=user_id, status=status, visibility=visibility)
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild",
                               real_name=species))
    db.add(CaptureLocation(submission_id=sub.id, latitude=lat, longitude=lng))
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild",
                      points=points, event_type="scored", new_state=status))
    db.commit()
    return sub


class TestMapSightings:
    def test_public_captures_appear_with_coarse_cells(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id=BETA))
        db_session.commit()
        _capture(db_session, BETA, "Capra falconeri", 33.7488, 73.1450)

        resp = client.get("/v1/map/sightings", headers=AUTH).json()
        assert resp["total"] == 1
        item = resp["items"][0]
        assert item["species"] == "Capra falconeri"
        assert item["scoreEvent"]["points"] == 40
        # Coarse 2-decimal cell, never the exact GPS.
        assert item["publicLocation"]["cellLatitude"] == 33.75
        assert item["publicLocation"]["cellLongitude"] == 73.14
        assert "33.7488" not in str(resp)

    def test_private_and_friends_hidden(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id=BETA))
        db_session.commit()
        _capture(db_session, BETA, "Vulpes vulpes", 33.7, 73.0,
                 visibility="private")
        _capture(db_session, BETA, "Axis axis", 33.7, 73.0,
                 visibility="friends")

        resp = client.get("/v1/map/sightings", headers=AUTH).json()
        assert resp["total"] == 0

    def test_sensitive_species_hidden(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id=BETA))
        db_session.add(SensitiveSpecies(scientific_name="Panthera uncia"))
        db_session.commit()
        _capture(db_session, BETA, "Panthera uncia", 35.0, 74.0)

        resp = client.get("/v1/map/sightings", headers=AUTH).json()
        assert resp["total"] == 0

    def test_blocked_users_excluded(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id=BETA))
        db_session.commit()
        _capture(db_session, BETA, "Milvus migrans", 33.72, 73.06)
        assert client.post(
            f"/v1/blocks/{BETA}", headers=AUTH
        ).status_code == 201

        resp = client.get("/v1/map/sightings", headers=AUTH).json()
        assert resp["total"] == 0
