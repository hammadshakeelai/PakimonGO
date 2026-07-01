import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .modules.leaderboard.api.routes import router as leaderboard_router
from .modules.media.api.routes import router as media_router
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    _start_worker_thread()
    yield


app = FastAPI(title="PakimonGO API", version="0.1.0", lifespan=lifespan)
app.include_router(leaderboard_router)
app.include_router(media_router)
app.include_router(submission_router)
app.include_router(users_router)


@app.get("/health/live")
def health_live():
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready():
    return {"status": "ok"}
