import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

def _resolve_database_url() -> str:
    # Managed Postgres hosts (Render, Heroku) expose a single connection URL.
    # Accept SYNC_DATABASE_URL first, then fall back to DATABASE_URL.
    raw = os.getenv("SYNC_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not raw:
        raw = (
            f"postgresql://{os.getenv('DB_USER', 'postgres')}"
            f":{os.getenv('DB_PASSWORD', 'dummy_local_password')}"
            f"@{os.getenv('DB_HOST', 'localhost')}"
            f":{os.getenv('DB_PORT', '5432')}"
            f"/{os.getenv('DB_NAME', 'pakimongo_local')}"
        )
    # SQLAlchemy 2.0 rejects the legacy "postgres://" scheme these hosts hand out.
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw[len("postgres://"):]
    return raw


SYNC_DATABASE_URL = _resolve_database_url()

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        connect_args = {}
        url = SYNC_DATABASE_URL
        if url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(url, pool_pre_ping=not url.startswith("sqlite"), connect_args=connect_args)
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=get_engine())


def drop_db():
    Base.metadata.drop_all(bind=get_engine())
