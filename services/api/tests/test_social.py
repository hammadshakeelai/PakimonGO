from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import (
    Base,
    ScoreEvent,
    Submission,
    SubmissionAttribute,
    User,
)
from src.infrastructure.database.session import get_db
from src.infrastructure.middleware.rate_limit import reset as reset_rate_limit
from src.main import app

AUTH = {"Authorization": "Bearer test_user_soc_alpha"}
AUTH_OTHER = {"Authorization": "Bearer test_user_soc_beta"}
ALPHA = "soc_alpha"
BETA = "soc_beta"


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
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    engine.dispose()
    db_path.unlink(missing_ok=True)


@pytest.fixture
def client(db_session):
    def _override():
        yield db_session

    reset_rate_limit()
    app.dependency_overrides[get_db] = _override
    yield TestClient(app)
    app.dependency_overrides.clear()
    reset_rate_limit()


def _seed(db):
    db.add(User(id=ALPHA))
    db.add(User(id=BETA))
    sub = Submission(user_id=BETA, status="scored")
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild", real_name="Sparrow"))
    db.add(
        ScoreEvent(
            submission_id=sub.id,
            user_id=BETA,
            ledger="wild",
            points=25,
            event_type="scored",
            new_state="scored",
        )
    )
    db.commit()
    return sub


class TestReactions:
    def test_react_then_toggle_off(self, db_session, client):
        sub = _seed(db_session)
        url = f"/v1/submissions/{sub.id}/reaction"
        resp = client.put(url, json={"kind": "wow"}, headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["myReaction"] == "wow"
        assert resp.json()["counts"] == {"wow": 1}
        # same kind again removes it
        resp = client.put(url, json={"kind": "wow"}, headers=AUTH)
        assert resp.json()["myReaction"] is None
        assert resp.json()["counts"] == {}

    def test_react_replaces_kind(self, db_session, client):
        sub = _seed(db_session)
        url = f"/v1/submissions/{sub.id}/reaction"
        client.put(url, json={"kind": "wow"}, headers=AUTH)
        resp = client.put(url, json={"kind": "cute"}, headers=AUTH)
        assert resp.json()["myReaction"] == "cute"
        assert resp.json()["counts"] == {"cute": 1}

    def test_invalid_kind_rejected(self, db_session, client):
        sub = _seed(db_session)
        resp = client.put(
            f"/v1/submissions/{sub.id}/reaction", json={"kind": "angry"}, headers=AUTH
        )
        assert resp.status_code == 400

    def test_missing_submission_404(self, db_session, client):
        _seed(db_session)
        resp = client.put(
            "/v1/submissions/nope/reaction", json={"kind": "wow"}, headers=AUTH
        )
        assert resp.status_code == 404

    def test_reaction_notifies_owner(self, db_session, client):
        sub = _seed(db_session)
        client.put(f"/v1/submissions/{sub.id}/reaction", json={"kind": "rare"}, headers=AUTH)
        resp = client.get("/v1/notifications", headers=AUTH_OTHER)
        types = [n["notificationType"] for n in resp.json()["items"]]
        assert "reaction" in types

    def test_feed_includes_reaction_aggregates(self, db_session, client):
        sub = _seed(db_session)
        client.put(f"/v1/submissions/{sub.id}/reaction", json={"kind": "wow"}, headers=AUTH)
        client.put(
            f"/v1/submissions/{sub.id}/reaction", json={"kind": "wow"}, headers=AUTH_OTHER
        )
        resp = client.get("/v1/feed", headers=AUTH)
        item = resp.json()["items"][0]
        assert item["reactionCounts"] == {"wow": 2}
        assert item["myReaction"] == "wow"
        assert item["commentCount"] == 0


class TestComments:
    def test_comment_lifecycle(self, db_session, client):
        sub = _seed(db_session)
        url = f"/v1/submissions/{sub.id}/comments"
        resp = client.post(url, json={"body": "Lovely shot!"}, headers=AUTH)
        assert resp.status_code == 201
        comment_id = resp.json()["commentId"]

        resp = client.get(url, headers=AUTH_OTHER)
        assert resp.json()["pagination"]["total"] == 1
        assert resp.json()["items"][0]["body"] == "Lovely shot!"

        # only the author can delete
        assert client.delete(f"/v1/comments/{comment_id}", headers=AUTH_OTHER).status_code == 404
        assert client.delete(f"/v1/comments/{comment_id}", headers=AUTH).status_code == 200
        resp = client.get(url, headers=AUTH)
        assert resp.json()["pagination"]["total"] == 0

    def test_empty_body_rejected(self, db_session, client):
        sub = _seed(db_session)
        resp = client.post(
            f"/v1/submissions/{sub.id}/comments", json={"body": "   "}, headers=AUTH
        )
        assert resp.status_code == 400

    def test_comment_notifies_owner_and_counts_in_feed(self, db_session, client):
        sub = _seed(db_session)
        client.post(
            f"/v1/submissions/{sub.id}/comments", json={"body": "Where was this?"}, headers=AUTH
        )
        resp = client.get("/v1/notifications", headers=AUTH_OTHER)
        types = [n["notificationType"] for n in resp.json()["items"]]
        assert "comment" in types
        resp = client.get("/v1/feed", headers=AUTH)
        assert resp.json()["items"][0]["commentCount"] == 1

    def test_comment_rate_limit(self, db_session, client):
        sub = _seed(db_session)
        url = f"/v1/submissions/{sub.id}/comments"
        for i in range(10):
            assert client.post(url, json={"body": f"c{i}"}, headers=AUTH).status_code == 201
        assert client.post(url, json={"body": "spam"}, headers=AUTH).status_code == 429


class TestPublicProfile:
    def test_public_profile(self, db_session, client):
        sub = _seed(db_session)
        resp = client.get(f"/v1/users/{BETA}/profile", headers=AUTH)
        assert resp.status_code == 200
        data = resp.json()
        assert data["userId"] == BETA
        assert data["totalPoints"] == 25
        assert data["captureCount"] == 1
        assert data["recentCaptures"][0]["submissionId"] == sub.id
        assert "email" not in data

    def test_unknown_user_404(self, db_session, client):
        _seed(db_session)
        assert client.get("/v1/users/ghost/profile", headers=AUTH).status_code == 404
