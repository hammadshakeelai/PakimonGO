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
from src.main import app

AUTH_A = {"Authorization": "Bearer test_user_fol_alpha"}
AUTH_B = {"Authorization": "Bearer test_user_fol_beta"}
ALPHA = "fol_alpha"
BETA = "fol_beta"


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


def _users(db):
    db.add(User(id=ALPHA))
    db.add(User(id=BETA))
    db.commit()


def _scored(db, user_id, visibility="public", species="Sparrow", points=25,
            lat=None, lng=None):
    from src.infrastructure.database.models import CaptureLocation

    sub = Submission(user_id=user_id, status="scored", visibility=visibility)
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild",
                               real_name=species))
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild",
                      points=points, event_type="scored", new_state="scored"))
    if lat is not None and lng is not None:
        db.add(CaptureLocation(submission_id=sub.id, latitude=lat, longitude=lng))
    db.commit()
    return sub


class TestFollow:
    def test_follow_unfollow_and_profile_counts(self, db_session, client):
        _users(db_session)
        # alpha follows beta
        assert client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A).status_code == 201
        # idempotent
        assert client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A).status_code == 201

        prof = client.get(f"/v1/users/{BETA}/profile", headers=AUTH_A).json()
        assert prof["followerCount"] == 1
        assert prof["isFollowing"] is True
        assert prof["isSelf"] is False

        own = client.get(f"/v1/users/{ALPHA}/profile", headers=AUTH_A).json()
        assert own["followingCount"] == 1
        assert own["isSelf"] is True

        assert client.delete(f"/v1/users/{BETA}/follow", headers=AUTH_A).status_code == 200
        prof = client.get(f"/v1/users/{BETA}/profile", headers=AUTH_A).json()
        assert prof["followerCount"] == 0
        assert prof["isFollowing"] is False

    def test_cannot_follow_self(self, db_session, client):
        _users(db_session)
        assert client.post(f"/v1/users/{ALPHA}/follow", headers=AUTH_A).status_code == 400

    def test_follow_missing_user_404(self, db_session, client):
        _users(db_session)
        assert client.post("/v1/users/ghost/follow", headers=AUTH_A).status_code == 404

    def test_new_follow_notifies_followee_once(self, db_session, client):
        _users(db_session)
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        # re-follow (idempotent) must NOT create a second notification
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        notes = client.get("/v1/notifications", headers=AUTH_B).json()["items"]
        follows = [n for n in notes if n["notificationType"] == "new_follower"]
        assert len(follows) == 1
        assert follows[0]["referenceType"] == "user"
        assert follows[0]["referenceId"] == ALPHA

    def test_followers_and_following_lists(self, db_session, client):
        _users(db_session)
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        followers = client.get(f"/v1/users/{BETA}/followers", headers=AUTH_A).json()
        assert followers["items"] == [ALPHA]
        following = client.get(f"/v1/users/{ALPHA}/following", headers=AUTH_A).json()
        assert following["items"] == [BETA]


class TestUserSearch:
    def test_search_matches_and_excludes_self(self, db_session, client):
        _users(db_session)
        db_session.add(User(id="ranger_bilal"))
        db_session.commit()
        _scored(db_session, "ranger_bilal", points=80)
        # alpha searches "ran" -> finds ranger_bilal, not itself
        resp = client.get("/v1/users/search?q=ran", headers=AUTH_A)
        ids = [u["userId"] for u in resp.json()["items"]]
        assert "ranger_bilal" in ids
        assert ALPHA not in ids
        assert resp.json()["items"][0]["totalPoints"] == 80

    def test_search_case_insensitive(self, db_session, client):
        _users(db_session)
        resp = client.get("/v1/users/search?q=BETA", headers=AUTH_A)
        assert BETA in [u["userId"] for u in resp.json()["items"]]

    def test_search_requires_query(self, db_session, client):
        _users(db_session)
        assert client.get("/v1/users/search?q=", headers=AUTH_A).status_code == 422


class TestFriendsVisibilityAndScope:
    def test_friends_post_visible_only_to_followers(self, db_session, client):
        _users(db_session)
        _scored(db_session, BETA, visibility="friends", species="Markhor")
        # alpha does not follow beta yet -> friends post hidden
        feed = client.get("/v1/feed", headers=AUTH_A).json()
        assert feed["items"] == []
        # after following, the friends post appears
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        feed = client.get("/v1/feed", headers=AUTH_A).json()
        assert len(feed["items"]) == 1
        assert feed["items"][0]["species"] == "Markhor"

    def test_following_scope_filters_feed(self, db_session, client):
        _users(db_session)
        _scored(db_session, BETA, visibility="public", species="Eagle")
        db_session.add(User(id="stranger"))
        db_session.commit()
        _scored(db_session, "stranger", visibility="public", species="Owl")
        # global feed shows both
        allf = client.get("/v1/feed", headers=AUTH_A).json()
        assert len(allf["items"]) == 2
        # following scope: alpha follows only beta
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        foll = client.get("/v1/feed?scope=following", headers=AUTH_A).json()
        species = {i["species"] for i in foll["items"]}
        assert species == {"Eagle"}

    def test_friends_leaderboard_scope(self, db_session, client):
        _users(db_session)
        _scored(db_session, ALPHA, points=10)
        _scored(db_session, BETA, points=50)
        db_session.add(User(id="stranger"))
        db_session.commit()
        _scored(db_session, "stranger", points=99)
        client.post(f"/v1/users/{BETA}/follow", headers=AUTH_A)
        board = client.get("/v1/leaderboard?scope=friends", headers=AUTH_A).json()
        ids = {e["userId"] for e in board["entries"]}
        assert ids == {ALPHA, BETA}  # self + followed, not stranger

    def test_local_leaderboard_scope(self, db_session, client):
        _users(db_session)
        db_session.add(User(id="faraway"))
        db_session.commit()
        # alpha + beta in the same ~11km cell; faraway elsewhere.
        _scored(db_session, ALPHA, points=10, lat=33.71, lng=73.06)
        _scored(db_session, BETA, points=50, lat=33.73, lng=73.09)
        _scored(db_session, "faraway", points=99, lat=31.52, lng=74.35)
        board = client.get("/v1/leaderboard?scope=local", headers=AUTH_A).json()
        ids = {e["userId"] for e in board["entries"]}
        assert ids == {ALPHA, BETA}  # same city cell, not faraway

    def test_local_scope_empty_without_captures(self, db_session, client):
        _users(db_session)  # alpha has no geolocated captures
        board = client.get("/v1/leaderboard?scope=local", headers=AUTH_A).json()
        assert board["entries"] == []
