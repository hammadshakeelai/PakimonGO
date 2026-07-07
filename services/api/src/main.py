import os
import threading
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .infrastructure.database.session import get_db

from .infrastructure.middleware.error_middleware import ErrorHandlingMiddleware, http_exception_handler
from .infrastructure.middleware.version_middleware import VersionNegotiationMiddleware
from .modules.leaderboard.api.routes import router as leaderboard_router
from .modules.media.api.routes import router as media_router
from .modules.moderation.api.routes import router as moderation_router
from .modules.notifications.api.routes import router as notification_router
from .modules.submissions.api.routes import router as submission_router
from .modules.users.api.routes import router as users_router


def _start_worker_thread():
    from src.infrastructure.worker.scoring_worker import process_pending_jobs
    from src.infrastructure.queue.queue import get_queue

    _POLL_INTERVAL = 0.5
    queue = get_queue()

    def _poll():
        while True:
            process_pending_jobs(queue)
            import time
            time.sleep(_POLL_INTERVAL)

    thread = threading.Thread(target=_poll, daemon=True)
    thread.start()
    return thread


def _run_demo_seed_if_enabled():
    """DEMO_SEED=1 seeds proof-of-concept content owned by the official
    demo user (idempotent; re-materializes files on ephemeral disks)."""
    if os.getenv("DEMO_SEED") != "1":
        return
    import sys
    from pathlib import Path

    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    sys.path.insert(0, str(scripts_dir))
    try:
        from demo_seed import run_demo_seed

        db = next(get_db())
        try:
            run_demo_seed(db)
        finally:
            db.close()
    except Exception:  # never block startup on demo content
        import traceback

        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_demo_seed_if_enabled()
    _start_worker_thread()
    yield


app = FastAPI(title="PakimonGO API", version="0.1.0", lifespan=lifespan)
_cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=_cors_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(VersionNegotiationMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.include_router(leaderboard_router, prefix="/v1")
app.include_router(media_router, prefix="/v1")
app.include_router(moderation_router, prefix="/v1")
app.include_router(notification_router, prefix="/v1")
app.include_router(submission_router, prefix="/v1")
app.include_router(users_router, prefix="/v1")


@app.get("/health/live")
def health_live():
    """Liveness check — always returns ok if server is running."""
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready(db: Session = Depends(get_db)):
    """Readiness check — verifies DB connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unreachable"},
        )
