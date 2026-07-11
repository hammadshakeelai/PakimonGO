"""In-process sliding-window rate limiter.

Correct for a single-instance deployment (Render free tier runs one
process); counters reset on restart, which is acceptable for spam
protection on write endpoints.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock

_windows: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def allow(key: str, max_calls: int, per_seconds: float) -> bool:
    """Return True if `key` may perform another call within its window."""
    now = time.monotonic()
    with _lock:
        window = _windows[key]
        cutoff = now - per_seconds
        while window and window[0] < cutoff:
            window.popleft()
        if len(window) >= max_calls:
            return False
        window.append(now)
        return True


def reset() -> None:
    """Clear all counters (tests only)."""
    with _lock:
        _windows.clear()
