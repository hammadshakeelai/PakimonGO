from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from demo_seed import DEMO_CAPTURES, DEMO_USER_ID, run_demo_seed  # noqa: E402
from src.infrastructure.database.models import (  # noqa: E402
    Base,
    CaptureLocation,
    MediaAsset,
    Notification,
    ScoreEvent,
    Submission,
)


@pytest.fixture
def db_session(tmp_path, monkeypatch):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Uploads land in a temp dir, not the repo.
    monkeypatch.setenv("UPLOAD_BASE", str(tmp_path / "uploads"))
    import src.infrastructure.storage.local_storage as ls
    monkeypatch.setattr(ls, "UPLOAD_BASE", tmp_path / "uploads")

    engine = create_engine(
        f"sqlite:///{tmp_path/'seed.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    engine.dispose()


def test_seed_creates_full_demo_content(db_session, tmp_path):
    created = run_demo_seed(db_session)
    assert created is True

    subs = db_session.query(Submission).filter(
        Submission.user_id == DEMO_USER_ID).all()
    assert len(subs) == len(DEMO_CAPTURES)
    assert all(s.status == "scored" for s in subs)

    # Every capture has a location, a score event, and stored files
    # (community accounts add their own locations on top).
    assert db_session.query(CaptureLocation).count() >= len(DEMO_CAPTURES)
    assert db_session.query(ScoreEvent).filter(
        ScoreEvent.user_id == DEMO_USER_ID).count() == len(DEMO_CAPTURES)
    # At least one per capture; the demo user also receives follow
    # notifications from the seeded social graph.
    assert db_session.query(Notification).filter(
        Notification.user_id == DEMO_USER_ID).count() >= len(DEMO_CAPTURES)

    assets = db_session.query(MediaAsset).filter(
        MediaAsset.owner_user_id == DEMO_USER_ID).all()
    assert len(assets) == len(DEMO_CAPTURES)
    for asset in assets:
        assert asset.processing_state == "ready"
        # Originals are stored extension-less; thumbs as .webp.
        assert (tmp_path / "uploads" / "originals" / asset.id).exists()
        assert (tmp_path / "uploads" / "thumbs" / f"{asset.id}.webp").exists()


def test_seed_is_idempotent(db_session):
    assert run_demo_seed(db_session) is True
    assert run_demo_seed(db_session) is False  # second run adds nothing
    assert db_session.query(Submission).filter(
        Submission.user_id == DEMO_USER_ID).count() == len(DEMO_CAPTURES)


def test_seed_restores_missing_files(db_session, tmp_path):
    run_demo_seed(db_session)
    originals = tmp_path / "uploads" / "originals"
    for f in originals.glob("media_*"):
        f.unlink()  # simulate ephemeral-disk wipe

    run_demo_seed(db_session)  # second boot restores files
    asset = db_session.query(MediaAsset).filter(
        MediaAsset.owner_user_id == DEMO_USER_ID).first()
    assert (originals / asset.id).exists()


def test_social_wave_seeds_photos_comments_reactions_stories(db_session):
    from datetime import datetime, timezone

    from demo_seed_graph import (
        COMMENTS2,
        FOLLOW_GRAPH,
        REACTIONS2,
        WAVE2,
        WAVE2_OWNERS,
    )
    from demo_seed_social import COMMENTS, REACTIONS, WAVE, WAVE_OWNERS
    from src.infrastructure.database.models import (
        Comment,
        Follow,
        Notification,
        Reaction,
        Story,
        User,
    )

    run_demo_seed(db_session)

    for owner in WAVE_OWNERS + WAVE2_OWNERS:
        assert db_session.query(User).filter(User.id == owner).first() is not None
    both = list(set(WAVE_OWNERS) | set(WAVE2_OWNERS))
    assert db_session.query(Submission).filter(
        Submission.user_id.in_(both)).count() == len(WAVE) + len(WAVE2)
    assert db_session.query(Comment).count() == len(COMMENTS) + len(COMMENTS2)
    assert db_session.query(Reaction).count() == len(REACTIONS) + len(REACTIONS2)
    # Follow graph seeded, each edge with a follower notification.
    assert db_session.query(Follow).count() == len(FOLLOW_GRAPH)
    assert db_session.query(Notification).filter(
        Notification.notification_type == "new_follower").count() == len(FOLLOW_GRAPH)
    # Every storyteller has one active story.
    now = datetime.now(timezone.utc)
    stories = db_session.query(Story).all()
    assert len(stories) == 4
    assert all(s.expires_at.replace(tzinfo=timezone.utc) > now for s in stories)

    # Second run adds nothing new (idempotent).
    run_demo_seed(db_session)
    assert db_session.query(Comment).count() == len(COMMENTS) + len(COMMENTS2)
    assert db_session.query(Reaction).count() == len(REACTIONS) + len(REACTIONS2)
    assert db_session.query(Follow).count() == len(FOLLOW_GRAPH)
    assert db_session.query(Story).count() == 4


def test_feed_returns_seeded_timeline(db_session):
    """/v1/feed serves the public timeline with coarse areas only."""
    from fastapi.testclient import TestClient
    from src.infrastructure.database.session import get_db
    from src.main import app

    run_demo_seed(db_session)

    def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    try:
        client = TestClient(app)
        resp = client.get("/v1/feed?limit=30")
        assert resp.status_code == 200
        data = resp.json()
        assert data["pagination"]["total"] >= len(DEMO_CAPTURES)
        item = data["items"][0]
        for key in ("submissionId", "userId", "mediaAssetId", "species",
                    "points", "caption"):
            assert key in item
        # Exact coordinates never appear — only 2-decimal cells.
        assert "latitude" not in item and "longitude" not in item
        # Many community accounts contribute to the timeline.
        assert data["pagination"]["total"] >= 40
        assert len({i["userId"] for i in data["items"]}) >= 4
    finally:
        app.dependency_overrides.clear()
