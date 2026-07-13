from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Submission


def get_capture_streak(db: Session, user_id: str) -> dict:
    """Daily capture streak computed from distinct UTC capture dates.

    - ``current``: consecutive days ending today (or yesterday, so a
      streak isn't shown as broken before the player has had a chance
      to capture today).
    - ``best``: longest consecutive run ever.
    - ``todayDone``: whether a scored capture landed today.
    """
    rows = (
        db.query(func.date(Submission.created_at))
        .filter(
            Submission.user_id == user_id,
            Submission.status.in_(["scored", "capped"]),
        )
        .distinct()
        .all()
    )
    days: set[date] = set()
    for (raw,) in rows:
        if raw is None:
            continue
        if isinstance(raw, datetime):
            days.add(raw.date())
        elif isinstance(raw, date):
            days.add(raw)
        else:  # SQLite returns ISO strings
            days.add(date.fromisoformat(str(raw)[:10]))
    if not days:
        return {"current": 0, "best": 0, "todayDone": False}

    ordered = sorted(days)
    best = run = 1
    for prev, cur in zip(ordered, ordered[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        best = max(best, run)

    today = datetime.now(timezone.utc).date()
    if today in days:
        anchor = today
    elif today - timedelta(days=1) in days:
        anchor = today - timedelta(days=1)
    else:
        anchor = None

    current = 0
    if anchor is not None:
        current = 1
        d = anchor - timedelta(days=1)
        while d in days:
            current += 1
            d -= timedelta(days=1)

    return {"current": current, "best": best, "todayDone": today in days}
