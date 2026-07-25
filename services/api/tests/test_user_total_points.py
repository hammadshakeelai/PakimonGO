from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base, ScoreEvent, Submission, User
from src.infrastructure.database.repositories.user import get_user_total_points
from src.infrastructure.database.session import get_db
from src.main import app

AUTH = {"Authorization": "Bearer test_user_pts_alpha"}
ALPHA = "pts_alpha"


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


def _scored(db, user_id, points, status="scored"):
    sub = Submission(user_id=user_id, status=status, visibility="public")
    db.add(sub)
    db.flush()
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild",
                       points=points, event_type="scored", new_state="scored"))
    db.commit()


class TestUserTotalPoints:
    def test_no_submissions_is_zero(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        assert get_user_total_points(db_session, ALPHA) == 0

    def test_sums_every_score_event(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        _scored(db_session, ALPHA, 25)
        _scored(db_session, ALPHA, 40)
        _scored(db_session, ALPHA, 5)
        assert get_user_total_points(db_session, ALPHA) == 70

    def test_ignores_other_users(self, db_session):
        db_session.add(User(id=ALPHA))
        db_session.add(User(id="pts_other"))
        db_session.commit()
        _scored(db_session, ALPHA, 25)
        _scored(db_session, "pts_other", 999)
        assert get_user_total_points(db_session, ALPHA) == 25

    def test_users_me_includes_total_points(self, db_session, client):
        db_session.add(User(id=ALPHA))
        db_session.commit()
        _scored(db_session, ALPHA, 25)
        _scored(db_session, ALPHA, 15)
        me = client.get("/v1/users/me", headers=AUTH).json()
        assert me["totalPoints"] == 40

    def test_users_me_total_points_zero_for_new_user(self, db_session, client):
        me = client.get("/v1/users/me", headers=AUTH).json()
        assert me["totalPoints"] == 0
