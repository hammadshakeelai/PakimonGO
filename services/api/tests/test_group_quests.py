from __future__ import annotations

from datetime import datetime, timedelta, timezone

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
from src.infrastructure.database.repositories.quest import create_quest
from src.infrastructure.database.session import get_db
from src.main import app

AUTH_A = {"Authorization": "Bearer test_user_qst_alpha"}
AUTH_C = {"Authorization": "Bearer test_user_qst_gamma"}
ALPHA = "qst_alpha"
BETA = "qst_beta"
GAMMA = "qst_gamma"  # not a member


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


def _seed_group(db):
    for uid in (ALPHA, BETA, GAMMA):
        db.add(User(id=uid))
    db.commit()
    g = create_group(db, "Quest Squad", description="Testers")
    add_member(db, g.id, ALPHA, role="admin")
    add_member(db, g.id, BETA)
    return g


def _scored(db, user_id, points, species="Markhor", created_at=None):
    sub = Submission(user_id=user_id, status="scored", visibility="public")
    if created_at is not None:
        sub.created_at = created_at
    db.add(sub)
    db.flush()
    db.add(SubmissionAttribute(submission_id=sub.id, animal_context="wild",
                               real_name=species))
    db.add(ScoreEvent(submission_id=sub.id, user_id=user_id, ledger="wild",
                      points=points, event_type="scored", new_state="scored"))
    db.commit()
    return sub


def _week_quest(db, group_id, kind, target, title="Test Quest"):
    now = datetime.now(timezone.utc)
    return create_quest(
        db, group_id, title, target,
        ends_at=now + timedelta(days=7), kind=kind,
        starts_at=now - timedelta(days=7), description="desc")


class TestGroupQuests:
    def test_captures_progress_and_my_contribution(self, db_session, client):
        g = _seed_group(db_session)
        _week_quest(db_session, g.id, "captures", 5)
        _scored(db_session, ALPHA, 30, species="Markhor")
        _scored(db_session, ALPHA, 20, species="Hoopoe")
        _scored(db_session, BETA, 40, species="Red Fox")
        _scored(db_session, GAMMA, 99, species="Koel")  # non-member: excluded

        resp = client.get(f"/v1/groups/{g.id}/quests", headers=AUTH_A).json()
        assert resp["total"] == 1
        quest = resp["items"][0]
        assert quest["kind"] == "captures"
        assert quest["progress"] == 3
        assert quest["myContribution"] == 2
        assert quest["completed"] is False
        assert quest["secondsLeft"] > 0

    def test_species_and_points_kinds(self, db_session, client):
        g = _seed_group(db_session)
        _week_quest(db_session, g.id, "species", 2, title="Species Hunt")
        _week_quest(db_session, g.id, "points", 60, title="Points Push")
        _scored(db_session, ALPHA, 30, species="Markhor")
        _scored(db_session, ALPHA, 20, species="Markhor")  # same species
        _scored(db_session, BETA, 40, species="Red Fox")

        items = client.get(f"/v1/groups/{g.id}/quests", headers=AUTH_A).json()["items"]
        by_title = {q["title"]: q for q in items}
        assert by_title["Species Hunt"]["progress"] == 2  # Markhor + Red Fox
        assert by_title["Species Hunt"]["completed"] is True
        assert by_title["Points Push"]["progress"] == 90
        assert by_title["Points Push"]["completed"] is True

    def test_window_excludes_old_captures(self, db_session, client):
        g = _seed_group(db_session)
        _week_quest(db_session, g.id, "captures", 5)
        old = datetime.now(timezone.utc) - timedelta(days=30)
        _scored(db_session, ALPHA, 30, created_at=old)
        _scored(db_session, ALPHA, 20)

        quest = client.get(f"/v1/groups/{g.id}/quests", headers=AUTH_A).json()["items"][0]
        assert quest["progress"] == 1

    def test_expired_quest_hidden(self, db_session, client):
        g = _seed_group(db_session)
        now = datetime.now(timezone.utc)
        create_quest(db_session, g.id, "Over", 5,
                     ends_at=now - timedelta(hours=1),
                     starts_at=now - timedelta(days=8))
        resp = client.get(f"/v1/groups/{g.id}/quests", headers=AUTH_A).json()
        assert resp["total"] == 0

    def test_non_member_sees_progress_but_no_contribution(self, db_session, client):
        g = _seed_group(db_session)
        _week_quest(db_session, g.id, "captures", 5)
        _scored(db_session, ALPHA, 30)
        _scored(db_session, GAMMA, 99)  # gamma's own capture doesn't count

        quest = client.get(f"/v1/groups/{g.id}/quests", headers=AUTH_C).json()["items"][0]
        assert quest["progress"] == 1
        assert quest["myContribution"] == 0

    def test_missing_group_404(self, db_session, client):
        _seed_group(db_session)
        assert client.get("/v1/groups/ghost/quests", headers=AUTH_A).status_code == 404


class TestQuestCompleteNotifications:
    def test_squad_notified_once_when_target_reached(self, db_session, client):
        from src.infrastructure.database.models import Notification
        from src.infrastructure.database.repositories.quest import (
            notify_completed_quests,
        )

        g = _seed_group(db_session)  # alpha + beta members
        _week_quest(db_session, g.id, "captures", 2)

        _scored(db_session, ALPHA, 30, species="Markhor")
        assert notify_completed_quests(db_session, ALPHA) == 0  # 1/2

        _scored(db_session, BETA, 40, species="Red Fox")
        assert notify_completed_quests(db_session, BETA) == 2  # both members

        notifs = db_session.query(Notification).filter(
            Notification.notification_type == "quest_complete").all()
        assert {n.user_id for n in notifs} == {ALPHA, BETA}
        assert all(n.reference_type == "group" for n in notifs)
        assert all(n.reference_id == g.id for n in notifs)

        # Overshooting later never re-fires for the same window.
        _scored(db_session, ALPHA, 20, species="Hoopoe")
        assert notify_completed_quests(db_session, ALPHA) == 0

    def test_non_member_captures_never_notify(self, db_session, client):
        from src.infrastructure.database.repositories.quest import (
            notify_completed_quests,
        )

        _seed_group(db_session)
        _scored(db_session, GAMMA, 99)
        assert notify_completed_quests(db_session, GAMMA) == 0
