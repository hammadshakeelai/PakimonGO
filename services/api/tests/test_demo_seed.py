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

    # Every capture has a location, a score event, and stored files.
    assert db_session.query(CaptureLocation).count() == len(DEMO_CAPTURES)
    assert db_session.query(ScoreEvent).filter(
        ScoreEvent.user_id == DEMO_USER_ID).count() == len(DEMO_CAPTURES)
    assert db_session.query(Notification).filter(
        Notification.user_id == DEMO_USER_ID).count() == len(DEMO_CAPTURES)

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
