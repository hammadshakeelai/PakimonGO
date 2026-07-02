import os
import tempfile

_db_path = os.path.join(tempfile.gettempdir(), "pakimongo_test.db")
os.environ["SYNC_DATABASE_URL"] = f"sqlite:///{_db_path}"
os.environ["UPLOAD_BASE"] = os.path.join(tempfile.gettempdir(), "pakimongo_test_uploads")

from src.infrastructure.database.models import Base  # noqa: E402
from src.infrastructure.database.session import get_engine  # noqa: E402

Base.metadata.create_all(bind=get_engine())


def pytest_sessionfinish(session):
    Base.metadata.drop_all(bind=get_engine())
    try:
        os.remove(_db_path)
    except OSError:
        pass
    import shutil
    upload_dir = os.environ["UPLOAD_BASE"]
    if os.path.isdir(upload_dir):
        shutil.rmtree(upload_dir, ignore_errors=True)
