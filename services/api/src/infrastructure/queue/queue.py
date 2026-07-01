import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol


@dataclass
class Job:
    job_id: str
    job_type: str
    payload: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class JobQueue(Protocol):
    def enqueue(self, job_type: str, payload: dict) -> Job:
        ...

    def dequeue(self) -> Job | None:
        ...

    @property
    def pending_count(self) -> int:
        ...


class InMemoryJobQueue:
    def __init__(self):
        self._jobs: list[Job] = []

    def enqueue(self, job_type: str, payload: dict) -> Job:
        job = Job(
            job_id=f"job_{uuid.uuid4().hex[:16]}",
            job_type=job_type,
            payload=dict(payload),
        )
        self._jobs.append(job)
        return job

    def dequeue(self) -> Job | None:
        if self._jobs:
            return self._jobs.pop(0)
        return None

    @property
    def pending_count(self) -> int:
        return len(self._jobs)


_queue: InMemoryJobQueue = InMemoryJobQueue()


def get_queue() -> InMemoryJobQueue:
    return _queue
