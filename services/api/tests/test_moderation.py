from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base, ScoreEvent, Submission, SubmissionAttribute, User
from src.infrastructure.database.session import get_db
from src.main import app

AUTH = {"Authorization": "Bearer test_user_mod_alpha"}
AUTH_OTHER = {"Authorization": "Bearer test_user_mod_beta"}
ALPHA = "mod_alpha"
BETA = "mod_beta"


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

    app.dependency_overrides[get_db] = _override
    yield TestClient(app)
    app.dependency_overrides.clear()


def _seed_users(db):
    db.add(User(id=ALPHA))
    db.add(User(id=BETA))
    db.commit()


def _seed_scored_submission(db, user_id: str, points: int = 25):
    sub = Submission(user_id=user_id, status="scored")
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild", real_name="Sparrow"))
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild", points=points, event_type="scored", new_state="scored"))
    db.commit()
    return sub


class TestReports:
    def test_report_submission(self, db_session, client):
        _seed_users(db_session)
        sub = _seed_scored_submission(db_session, BETA)
        resp = client.post(
            "/v1/reports",
            json={"targetType": "submission", "targetId": sub.id, "reason": "inappropriate"},
            headers=AUTH,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["targetType"] == "submission"
        assert data["reason"] == "inappropriate"
        assert data["status"] == "open"

    def test_report_user(self, db_session, client):
        _seed_users(db_session)
        resp = client.post(
            "/v1/reports",
            json={"targetType": "user", "targetId": BETA, "reason": "harassment", "details": "abusive captions"},
            headers=AUTH,
        )
        assert resp.status_code == 201

    def test_duplicate_report_conflicts(self, db_session, client):
        _seed_users(db_session)
        body = {"targetType": "user", "targetId": BETA, "reason": "spam"}
        assert client.post("/v1/reports", json=body, headers=AUTH).status_code == 201
        assert client.post("/v1/reports", json=body, headers=AUTH).status_code == 409

    def test_invalid_reason_rejected(self, db_session, client):
        _seed_users(db_session)
        resp = client.post(
            "/v1/reports",
            json={"targetType": "user", "targetId": BETA, "reason": "i_just_dislike_them"},
            headers=AUTH,
        )
        assert resp.status_code == 400

    def test_invalid_target_type_rejected(self, client):
        resp = client.post(
            "/v1/reports",
            json={"targetType": "planet", "targetId": "earth", "reason": "spam"},
            headers=AUTH,
        )
        assert resp.status_code == 400

    def test_cannot_report_self(self, db_session, client):
        _seed_users(db_session)
        resp = client.post(
            "/v1/reports",
            json={"targetType": "user", "targetId": ALPHA, "reason": "spam"},
            headers=AUTH,
        )
        assert resp.status_code == 400

    def test_report_requires_auth(self, client):
        resp = client.post(
            "/v1/reports",
            json={"targetType": "user", "targetId": BETA, "reason": "spam"},
        )
        assert resp.status_code in (401, 403)


class TestBlocks:
    def test_block_and_list(self, db_session, client):
        _seed_users(db_session)
        resp = client.post(f"/v1/blocks/{BETA}", headers=AUTH)
        assert resp.status_code == 201
        assert resp.json()["blockedUserId"] == BETA

        listing = client.get("/v1/blocks", headers=AUTH).json()
        assert listing["total"] == 1
        assert listing["items"][0]["blockedUserId"] == BETA

    def test_block_is_idempotent(self, db_session, client):
        _seed_users(db_session)
        assert client.post(f"/v1/blocks/{BETA}", headers=AUTH).status_code == 201
        assert client.post(f"/v1/blocks/{BETA}", headers=AUTH).status_code == 201
        assert client.get("/v1/blocks", headers=AUTH).json()["total"] == 1

    def test_cannot_block_self(self, db_session, client):
        _seed_users(db_session)
        assert client.post(f"/v1/blocks/{ALPHA}", headers=AUTH).status_code == 400

    def test_block_unknown_user_404(self, db_session, client):
        _seed_users(db_session)
        assert client.post("/v1/blocks/who_dis", headers=AUTH).status_code == 404

    def test_unblock(self, db_session, client):
        _seed_users(db_session)
        client.post(f"/v1/blocks/{BETA}", headers=AUTH)
        assert client.delete(f"/v1/blocks/{BETA}", headers=AUTH).status_code == 200
        assert client.get("/v1/blocks", headers=AUTH).json()["total"] == 0

    def test_unblock_missing_404(self, db_session, client):
        _seed_users(db_session)
        assert client.delete(f"/v1/blocks/{BETA}", headers=AUTH).status_code == 404

    def test_blocks_are_per_user(self, db_session, client):
        _seed_users(db_session)
        client.post(f"/v1/blocks/{BETA}", headers=AUTH)
        assert client.get("/v1/blocks", headers=AUTH_OTHER).json()["total"] == 0


class TestBlockLeaderboardFiltering:
    def test_blocked_user_hidden_from_leaderboard(self, db_session, client):
        _seed_users(db_session)
        _seed_scored_submission(db_session, ALPHA, points=30)
        _seed_scored_submission(db_session, BETA, points=99)

        before = client.get("/v1/leaderboard", headers=AUTH).json()
        assert {e["userId"] for e in before["entries"]} == {ALPHA, BETA}

        client.post(f"/v1/blocks/{BETA}", headers=AUTH)

        after = client.get("/v1/leaderboard", headers=AUTH).json()
        assert {e["userId"] for e in after["entries"]} == {ALPHA}

        # The blocked user still sees everyone (block is one-directional).
        other_view = client.get("/v1/leaderboard", headers=AUTH_OTHER).json()
        assert {e["userId"] for e in other_view["entries"]} == {ALPHA, BETA}

    def test_anonymous_leaderboard_unfiltered(self, db_session, client):
        _seed_users(db_session)
        _seed_scored_submission(db_session, ALPHA)
        resp = client.get("/v1/leaderboard")
        assert resp.status_code == 200


class TestModerationAudit:
    def test_report_and_block_write_audit_rows(self, db_session, client):
        from src.infrastructure.database.models import AuditLog

        _seed_users(db_session)
        client.post(
            "/v1/reports",
            json={"targetType": "user", "targetId": BETA, "reason": "spam"},
            headers=AUTH,
        )
        client.post(f"/v1/blocks/{BETA}", headers=AUTH)
        client.delete(f"/v1/blocks/{BETA}", headers=AUTH)

        actions = [a.action for a in db_session.query(AuditLog).all()]
        assert "report_created" in actions
        assert "user_blocked" in actions
        assert "user_unblocked" in actions
