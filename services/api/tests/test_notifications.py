from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base, Notification
from src.infrastructure.database.repositories import create_notification
from src.infrastructure.database.session import get_db
from src.main import app

AUTH = {"Authorization": "Bearer test_user_notif"}
NOTIF_USER = "notif"


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


class TestNotificationRoutes:
    def test_list_empty(self, client):
        resp = client.get("/v1/notifications", headers=AUTH)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_notifications(self, db_session, client):
        create_notification(
            db=db_session, user_id=NOTIF_USER, notification_type="submission_scored",
            title="Scored", body="+25 pts", reference_type="submission", reference_id="s1",
        )
        resp = client.get("/v1/notifications", headers=AUTH)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Scored"
        assert data["items"][0]["isRead"] is False

    def test_unread_count(self, db_session, client):
        create_notification(db=db_session, user_id=NOTIF_USER, notification_type="t", title="A")
        create_notification(db=db_session, user_id=NOTIF_USER, notification_type="t", title="B")
        resp = client.get("/v1/notifications/unread-count", headers=AUTH)
        assert resp.json()["count"] == 2

    def test_mark_read(self, db_session, client):
        n = create_notification(db=db_session, user_id=NOTIF_USER, notification_type="t", title="R")
        resp = client.patch(f"/v1/notifications/{n.id}/read", headers=AUTH)
        assert resp.json()["notification"]["isRead"] is True
        resp2 = client.get("/v1/notifications/unread-count", headers=AUTH)
        assert resp2.json()["count"] == 0

    def test_mark_read_not_found(self, client):
        resp = client.patch("/v1/notifications/nonexistent/read", headers=AUTH)
        assert resp.json()["status"] == "not_found"

    def test_unread_only_filter(self, db_session, client):
        n = create_notification(db=db_session, user_id=NOTIF_USER, notification_type="t", title="X")
        n.is_read = True
        db_session.commit()
        create_notification(db=db_session, user_id=NOTIF_USER, notification_type="t", title="Y")
        resp = client.get("/v1/notifications?unread_only=true", headers=AUTH)
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Y"
