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
from src.infrastructure.database.repositories.group import add_member, create_group
from src.infrastructure.database.session import get_db
from src.main import app

AUTH_A = {"Authorization": "Bearer test_user_grp_alpha"}
AUTH_B = {"Authorization": "Bearer test_user_grp_beta"}
ALPHA = "grp_alpha"
BETA = "grp_beta"


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


def _seed(db):
    db.add(User(id=ALPHA))
    db.add(User(id=BETA))
    db.commit()
    g = create_group(db, "Islamabad Wildlife Squad", description="Capital critters",
                     cover_asset="markhor.jpg", created_by=BETA)
    add_member(db, g.id, BETA, role="admin")
    return g


def _scored(db, user_id, points):
    sub = Submission(user_id=user_id, status="scored", visibility="public")
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild",
                               real_name="Markhor"))
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild",
                      points=points, event_type="scored", new_state="scored"))
    db.commit()
    return sub


class TestGroups:
    def test_list_and_detail_with_membership(self, db_session, client):
        g = _seed(db_session)
        resp = client.get("/v1/groups", headers=AUTH_A).json()
        assert resp["total"] == 1
        item = resp["items"][0]
        assert item["name"] == "Islamabad Wildlife Squad"
        assert item["memberCount"] == 1  # beta
        assert item["isMember"] is False  # alpha not a member

        detail = client.get(f"/v1/groups/{g.id}", headers=AUTH_B).json()
        assert detail["isMember"] is True  # beta is a member

    def test_join_and_leave(self, db_session, client):
        g = _seed(db_session)
        assert client.post(f"/v1/groups/{g.id}/join", headers=AUTH_A).status_code == 201
        # idempotent
        assert client.post(f"/v1/groups/{g.id}/join", headers=AUTH_A).status_code == 201
        detail = client.get(f"/v1/groups/{g.id}", headers=AUTH_A).json()
        assert detail["isMember"] is True
        assert detail["memberCount"] == 2

        members = client.get(f"/v1/groups/{g.id}/members", headers=AUTH_A).json()
        assert set(members["items"]) == {ALPHA, BETA}

        assert client.delete(f"/v1/groups/{g.id}/join", headers=AUTH_A).status_code == 200
        assert client.get(f"/v1/groups/{g.id}", headers=AUTH_A).json()["memberCount"] == 1

    def test_leave_when_not_member_404(self, db_session, client):
        g = _seed(db_session)
        assert client.delete(f"/v1/groups/{g.id}/join", headers=AUTH_A).status_code == 404

    def test_missing_group_404(self, db_session, client):
        _seed(db_session)
        assert client.get("/v1/groups/ghost", headers=AUTH_A).status_code == 404

    def test_group_leaderboard_scoped_to_members(self, db_session, client):
        g = _seed(db_session)  # beta is a member
        client.post(f"/v1/groups/{g.id}/join", headers=AUTH_A)  # alpha joins
        db_session.add(User(id="outsider"))
        db_session.commit()
        _scored(db_session, ALPHA, 30)
        _scored(db_session, BETA, 70)
        _scored(db_session, "outsider", 99)
        board = client.get(f"/v1/groups/{g.id}/leaderboard", headers=AUTH_A).json()
        ids = {e["userId"] for e in board["entries"]}
        assert ids == {ALPHA, BETA}  # outsider excluded

    def test_group_feed_shows_member_captures(self, db_session, client):
        g = _seed(db_session)
        client.post(f"/v1/groups/{g.id}/join", headers=AUTH_A)
        db_session.add(User(id="outsider"))
        db_session.commit()
        _scored(db_session, ALPHA, 30)
        _scored(db_session, "outsider", 99)
        feed = client.get(f"/v1/groups/{g.id}/feed", headers=AUTH_A).json()
        users = {i["userId"] for i in feed["items"]}
        assert users == {ALPHA}  # only members, not outsider


class TestGroupCreation:
    def test_create_group_makes_creator_admin(self, db_session, client):
        from src.infrastructure.middleware.rate_limit import reset
        reset()
        _seed(db_session)
        resp = client.post(
            "/v1/groups",
            json={"name": "Night Owls", "description": "Nocturnal spotters"},
            headers=AUTH_A)
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "Night Owls"
        assert body["isMember"] is True
        assert body["memberCount"] == 1

        listing = client.get("/v1/groups", headers=AUTH_A).json()
        assert listing["total"] == 2  # seed group + the new one

        members = client.get(
            f"/v1/groups/{body['groupId']}/members", headers=AUTH_A).json()
        assert members["items"] == [ALPHA]

    def test_duplicate_name_conflict(self, db_session, client):
        from src.infrastructure.middleware.rate_limit import reset
        reset()
        _seed(db_session)
        resp = client.post(
            "/v1/groups", json={"name": "Islamabad Wildlife Squad"},
            headers=AUTH_A)
        assert resp.status_code == 409

    def test_name_too_short_rejected(self, db_session, client):
        from src.infrastructure.middleware.rate_limit import reset
        reset()
        _seed(db_session)
        assert client.post(
            "/v1/groups", json={"name": "ab"}, headers=AUTH_A
        ).status_code == 400


class TestGroupCover:
    def test_cover_is_latest_member_public_capture(self, db_session, client):
        g = _seed(db_session)  # beta is a member
        first = _scored(db_session, BETA, 30)
        first.primary_media_asset_id = "asset_first"
        latest = _scored(db_session, BETA, 55)
        latest.primary_media_asset_id = "asset_latest"
        db_session.commit()

        detail = client.get(f"/v1/groups/{g.id}", headers=AUTH_A).json()
        assert detail["coverMediaAssetId"] == "asset_latest"

    def test_cover_none_without_member_captures(self, db_session, client):
        g = _seed(db_session)
        detail = client.get(f"/v1/groups/{g.id}", headers=AUTH_A).json()
        assert detail["coverMediaAssetId"] is None
