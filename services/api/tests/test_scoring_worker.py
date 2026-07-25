"""Scoring worker resilience: a failing job must never take down the
worker loop, must eventually land in the existing REVIEW state instead
of vanishing, and a submission orphaned by a lost in-memory queue must
be recoverable at boot. See docs/TECH_DEBT.md / REMAINING_WORK.md -
"Scoring worker is in-process ... no persistence, no retries, no DLQ".
"""
from __future__ import annotations

import sys
from pathlib import Path

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient

from src.infrastructure.queue.queue import InMemoryJobQueue, get_queue
from src.infrastructure.worker.scoring_worker import (
    MAX_JOB_ATTEMPTS,
    process_pending_jobs,
    recover_orphaned_jobs,
)
from src.main import app

_score_pkg = Path(__file__).resolve().parents[3] / "packages" / "scoring-rules" / "src"
sys.path.insert(0, str(_score_pkg))

from scoring_service import ScoringResult  # noqa: E402

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer test_user_worker"}


class _FlakyScoringService:
    """Fails on call numbers in `fail_on` (1-indexed), succeeds otherwise -
    or fails on every call if `always_fail` is set."""

    def __init__(self, fail_on: set[int] | None = None, always_fail: bool = False):
        self.calls = 0
        self.fail_on = fail_on or set()
        self.always_fail = always_fail

    def evaluate(self, animal_context, explanation_category, media_path=None):
        self.calls += 1
        if self.always_fail or self.calls in self.fail_on:
            raise RuntimeError("simulated scoring failure")
        return ScoringResult(
            points=25, ledger="wild",
            explanation_category="normal", formula_version="test-v1",
        )


def _create_upload(sha_suffix: str):
    sha = sha_suffix * 64
    resp = client.post("/v1/media/upload-intent", json={
        "fileName": "worker.jpg",
        "contentType": "image/jpeg",
        "byteSize": 500000,
        "sha256": sha,
    }, headers=AUTH_HEADER)
    return resp.json()["mediaAssetId"]


def _create_wild_submission(sha_suffix: str) -> str:
    resp = client.post("/v1/submissions", json={
        "mediaAssetId": _create_upload(sha_suffix),
        "animalContext": "wild",
        "realName": "House Sparrow",
        "cuteName": "Worker Test",
        "caption": "worker test fixture",
        "tags": [],
    }, headers=AUTH_HEADER)
    assert resp.status_code == 200
    return resp.json()["submissionId"]


def _status(submission_id: str) -> str:
    resp = client.get(f"/v1/submissions/{submission_id}", headers=AUTH_HEADER)
    return resp.json()["scoreState"]["status"]


def _flush_singleton_queue():
    """Other test files share the same InMemoryJobQueue singleton - drain
    whatever is already pending (with the real scoring service) before a
    test relies on precise call-count/order behavior of an injected fake."""
    while get_queue().pending_count:
        process_pending_jobs(get_queue())


def test_a_failing_job_does_not_block_other_jobs_in_the_same_batch():
    _flush_singleton_queue()
    failing_id = _create_wild_submission("f1")
    healthy_id = _create_wild_submission("f2")
    queue = get_queue()
    assert queue.pending_count == 2

    # First call in this fake fails (the `failing_id` job, dequeued first -
    # FIFO), second call succeeds (the `healthy_id` job).
    svc = _FlakyScoringService(fail_on={1})
    processed = process_pending_jobs(queue, svc)

    assert processed == 2
    assert _status(healthy_id) == "scored"
    # The failed job was re-enqueued for the next tick, not lost or retried
    # within this same call (which would spin instead of backing off).
    assert queue.pending_count == 1
    assert _status(failing_id) == "ai_evaluated"

    # Draining again with a working service lets the retried job succeed.
    _flush_singleton_queue()
    assert _status(failing_id) == "scored"


def test_a_persistently_failing_job_lands_in_review_after_max_attempts():
    _flush_singleton_queue()
    submission_id = _create_wild_submission("f3")
    queue = get_queue()
    always_fails = _FlakyScoringService(always_fail=True)

    for _ in range(MAX_JOB_ATTEMPTS):
        process_pending_jobs(queue, always_fails)

    assert _status(submission_id) == "review"
    assert queue.pending_count == 0

    detail = client.get(f"/v1/submissions/{submission_id}", headers=AUTH_HEADER).json()
    assert detail["scoreState"]["visiblePoints"] is None


def test_recover_orphaned_jobs_reenqueues_a_submission_stuck_at_ai_evaluated():
    # Simulate a server restart: the submission's DB status is already
    # durably "ai_evaluated" (written before the in-memory enqueue), but
    # the queue that would have processed it is gone - modeled here with
    # a brand-new queue instance the singleton never touches.
    submission_id = _create_wild_submission("f4")
    assert _status(submission_id) == "ai_evaluated"

    recovery_queue = InMemoryJobQueue()
    recovered = recover_orphaned_jobs(recovery_queue)
    assert recovered >= 1
    assert recovery_queue.pending_count >= 1

    process_pending_jobs(recovery_queue)
    assert _status(submission_id) == "scored"
