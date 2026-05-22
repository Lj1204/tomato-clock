from __future__ import annotations

import time
from typing import Any

from src.timer.state import DEFAULT_DURATION_SEC


def _now() -> float:
    return time.time()


def tick(session_state: Any) -> None:
    """Apply elapsed wall-clock seconds to remaining time when timer is running."""
    if session_state.timer_status != "running":
        return

    now = _now()
    if session_state.last_tick_ts is None:
        # First tick after start/resume: anchor the baseline timestamp.
        session_state.last_tick_ts = now
        return

    # Use integer seconds to avoid visual jitter from sub-second updates.
    elapsed = int(now - session_state.last_tick_ts)
    if elapsed <= 0:
        return

    session_state.remaining_sec = max(0, session_state.remaining_sec - elapsed)
    session_state.last_tick_ts += elapsed

    if session_state.remaining_sec == 0:
        # Stage 1 behavior: stop at completion; stats are handled in later stages.
        session_state.timer_status = "idle"
        session_state.last_tick_ts = None


def start(session_state: Any) -> None:
    """Start countdown from current remaining time."""
    if session_state.timer_status == "running":
        return
    session_state.timer_status = "running"
    session_state.last_tick_ts = _now()


def pause(session_state: Any) -> None:
    """Freeze current progress and switch to paused state."""
    tick(session_state)
    session_state.timer_status = "paused"
    session_state.last_tick_ts = None


def resume(session_state: Any) -> None:
    """Continue countdown from paused position."""
    if session_state.timer_status != "paused":
        return
    session_state.timer_status = "running"
    session_state.last_tick_ts = _now()


def reset(session_state: Any) -> None:
    """Return to a fresh 25:00 idle state."""
    session_state.duration_sec = DEFAULT_DURATION_SEC
    session_state.remaining_sec = DEFAULT_DURATION_SEC
    session_state.timer_status = "idle"
    session_state.last_tick_ts = None
