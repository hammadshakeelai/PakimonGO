from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base, MediaAsset, Story, User
from src.infrastructure.database.session import get_db
from src.infrastructure.middleware.rate_limit import reset as reset_rate_limit
from src.main import app

AUTH = {"Authorization": "Bearer test_user_story_alpha"}
AUTH_OTHER = {"Authorization": "Bearer test_user_story_beta"}
ALPHA = "story_alpha"
BETA = "story_beta"


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
    asset = MediaAsset(owner_user_id=ALPHA, file_name="s.jpg", processing_state="ready")
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


class TestStories:
    def test_post_and_list_story(self, db_session, client):
        asset = _seed(db_session)
        resp = client.post(
            "/v1/stories",
            json={"mediaAssetId": asset.id, "caption": "Golden hour!"},
            headers=AUTH,
        )
        assert resp.status_code == 201
        story_id = resp.json()["storyId"]

        resp = client.get("/v1/stories", headers=AUTH_OTHER)
        groups = resp.json()["groups"]
        assert len(groups) == 1
        assert groups[0]["userId"] == ALPHA
        assert groups[0]["allSeen"] is False
        assert groups[0]["stories"][0]["storyId"] == story_id
        assert groups[0]["stories"][0]["seen"] is False

    def test_cannot_post_with_foreign_asset(self, db_session, client):
        asset = _seed(db_session)
        resp = client.post(
            "/v1/stories", json={"mediaAssetId": asset.id}, headers=AUTH_OTHER
        )
        assert resp.status_code == 404

    def test_view_marks_seen_and_lists_viewers(self, db_session, client):
        asset = _seed(db_session)
        story_id = client.post(
            "/v1/stories", json={"mediaAssetId": asset.id}, headers=AUTH
        ).json()["storyId"]

        assert client.post(f"/v1/stories/{story_id}/view", headers=AUTH_OTHER).status_code == 200
        # idempotent
        assert client.post(f"/v1/stories/{story_id}/view", headers=AUTH_OTHER).status_code == 200

        groups = client.get("/v1/stories", headers=AUTH_OTHER).json()["groups"]
        assert groups[0]["allSeen"] is True
        assert groups[0]["stories"][0]["seen"] is True

        # owner sees exactly one viewer
        views = client.get(f"/v1/stories/{story_id}/views", headers=AUTH).json()
        assert views["total"] == 1
        assert views["items"][0]["viewerId"] == BETA
        # non-owner cannot see viewers
        assert client.get(f"/v1/stories/{story_id}/views", headers=AUTH_OTHER).status_code == 404

    def test_owner_can_delete_story(self, db_session, client):
        asset = _seed(db_session)
        story_id = client.post(
            "/v1/stories", json={"mediaAssetId": asset.id}, headers=AUTH
        ).json()["storyId"]
        client.post(f"/v1/stories/{story_id}/view", headers=AUTH_OTHER)

        # only the owner can delete
        assert client.delete(f"/v1/stories/{story_id}", headers=AUTH_OTHER).status_code == 404
        assert client.delete(f"/v1/stories/{story_id}", headers=AUTH).status_code == 200
        assert client.get("/v1/stories", headers=AUTH_OTHER).json()["groups"] == []

    def test_expired_stories_hidden(self, db_session, client):
        asset = _seed(db_session)
        db_session.add(
            Story(
                user_id=ALPHA,
                media_asset_id=asset.id,
                expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            )
        )
        db_session.commit()
        resp = client.get("/v1/stories", headers=AUTH_OTHER)
        assert resp.json()["groups"] == []

    def test_own_ring_sorted_first(self, db_session, client):
        asset = _seed(db_session)
        beta_asset = MediaAsset(owner_user_id=BETA, file_name="b.jpg", processing_state="ready")
        db_session.add(beta_asset)
        db_session.commit()
        db_session.refresh(beta_asset)
        client.post("/v1/stories", json={"mediaAssetId": asset.id}, headers=AUTH)
        client.post("/v1/stories", json={"mediaAssetId": beta_asset.id}, headers=AUTH_OTHER)
        groups = client.get("/v1/stories", headers=AUTH).json()["groups"]
        assert groups[0]["userId"] == ALPHA
        assert groups[0]["stories"][0]["isMine"] is True

    def test_missing_media_asset_id_400(self, db_session, client):
        _seed(db_session)
        assert client.post("/v1/stories", json={}, headers=AUTH).status_code == 400


class TestStoryReactions:
    def _story(self, db, client):
        asset = _seed(db)
        return client.post(
            "/v1/stories", json={"mediaAssetId": asset.id}, headers=AUTH
        ).json()["storyId"]

    def test_react_notifies_owner_once(self, db_session, client):
        story_id = self._story(db_session, client)
        resp = client.post(
            f"/v1/stories/{story_id}/react", json={"emoji": "fire"},
            headers=AUTH_OTHER)
        assert resp.status_code == 201
        assert resp.json()["emoji"] == "fire"

        notifs = client.get("/v1/notifications", headers=AUTH).json()["items"]
        reactions = [n for n in notifs
                     if n["notificationType"] == "story_reaction"]
        assert len(reactions) == 1
        assert reactions[0]["referenceId"] == BETA

        # Re-reacting replaces the emoji without a second notification.
        resp = client.post(
            f"/v1/stories/{story_id}/react", json={"emoji": "heart"},
            headers=AUTH_OTHER)
        assert resp.status_code == 201
        notifs = client.get("/v1/notifications", headers=AUTH).json()["items"]
        assert len([n for n in notifs
                    if n["notificationType"] == "story_reaction"]) == 1

    def test_owner_sees_reactions_in_views(self, db_session, client):
        story_id = self._story(db_session, client)
        client.post(f"/v1/stories/{story_id}/view", headers=AUTH_OTHER)
        client.post(f"/v1/stories/{story_id}/react", json={"emoji": "clap"},
                    headers=AUTH_OTHER)
        views = client.get(f"/v1/stories/{story_id}/views",
                           headers=AUTH).json()["items"]
        assert views[0]["viewerId"] == BETA
        assert views[0]["reaction"] == "clap"

    def test_cannot_react_to_own_story(self, db_session, client):
        story_id = self._story(db_session, client)
        resp = client.post(f"/v1/stories/{story_id}/react",
                           json={"emoji": "wow"}, headers=AUTH)
        assert resp.status_code == 400

    def test_invalid_emoji_rejected(self, db_session, client):
        story_id = self._story(db_session, client)
        resp = client.post(f"/v1/stories/{story_id}/react",
                           json={"emoji": "skull"}, headers=AUTH_OTHER)
        assert resp.status_code == 400

    def test_missing_story_404(self, db_session, client):
        _seed(db_session)
        resp = client.post("/v1/stories/ghost/react",
                           json={"emoji": "fire"}, headers=AUTH_OTHER)
        assert resp.status_code == 404
