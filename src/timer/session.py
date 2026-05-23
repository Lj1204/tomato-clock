from __future__ import annotations

from typing import Any

from src.timer.state import create_default_state


STATE_KEYS = (
    "duration_sec",
    "remaining_sec",
    "timer_status",
    "last_tick_ts",
)


def ensure_timer_state(session_state: Any) -> None:
    """Initialize timer-related keys exactly once per user session."""
    default = create_default_state()
    if all(key in session_state for key in STATE_KEYS):
        # Force-sync when configured default duration changes.
        # This makes code-level duration edits take effect on next app start.
        if session_state.duration_sec != default.duration_sec:
            session_state.duration_sec = default.duration_sec
            session_state.remaining_sec = default.remaining_sec
            session_state.timer_status = default.timer_status
            session_state.last_tick_ts = default.last_tick_ts
        return

    session_state.duration_sec = default.duration_sec
    session_state.remaining_sec = default.remaining_sec
    session_state.timer_status = default.timer_status
    session_state.last_tick_ts = default.last_tick_ts
