from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base, Submission, User
from src.infrastructure.database.repositories.streak import get_capture_streak
from src.infrastructure.database.session import get_db
from src.main import app

AUTH = {"Authorization": "Bearer test_user_stk_alpha"}
ALPHA = "stk_alpha"


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


def _capture_on(db, user_id, days_ago, status="scored"):
    when = datetime.now(timezone.utc) - timedelta(days=days_ago)
    sub = Submission(user_id=user_id, status=status, visibility="public")
    sub.created_at = when
    db.add(sub)
    db.commit()


class TestStreak:
    def test_no_captures_is_zero(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        assert get_capture_streak(db_session, ALPHA) == {
            "current": 0, "best": 0, "todayDone": False}

    def test_run_ending_today(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        for days_ago in (0, 1, 2):
            _capture_on(db_session, ALPHA, days_ago)
        streak = get_capture_streak(db_session, ALPHA)
        assert streak["current"] == 3
        assert streak["best"] == 3
        assert streak["todayDone"] is True

    def test_streak_alive_through_yesterday(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        for days_ago in (1, 2):
            _capture_on(db_session, ALPHA, days_ago)
        streak = get_capture_streak(db_session, ALPHA)
        assert streak["current"] == 2  # not broken until today ends
        assert streak["todayDone"] is False

    def test_gap_breaks_current_but_keeps_best(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        for days_ago in (0, 5, 6, 7, 8):  # old 4-day run, fresh 1-day run
            _capture_on(db_session, ALPHA, days_ago)
        streak = get_capture_streak(db_session, ALPHA)
        assert streak["current"] == 1
        assert streak["best"] == 4

    def test_multiple_captures_one_day_count_once(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        _capture_on(db_session, ALPHA, 0)
        _capture_on(db_session, ALPHA, 0)
        assert get_capture_streak(db_session, ALPHA)["current"] == 1

    def test_pending_submissions_do_not_count(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        _capture_on(db_session, ALPHA, 0, status="pending")
        assert get_capture_streak(db_session, ALPHA)["current"] == 0

    def test_users_me_includes_streak(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        _capture_on(db_session, ALPHA, 0)
        me = client.get("/v1/users/me", headers=AUTH).json()
        assert me["streak"]["current"] == 1
        assert me["streak"]["todayDone"] is True

    def test_public_profile_includes_streak(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id="stk_viewer"))
        db_session.commit()
        _capture_on(db_session, ALPHA, 0)
        profile = client.get(
            f"/v1/users/{ALPHA}/profile",
            headers={"Authorization": "Bearer test_user_stk_viewer"},
        ).json()
        assert profile["streak"]["current"] == 1
