from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Timer status is intentionally small and explicit, so UI branching is simple.
TimerStatus = Literal["idle", "running", "paused"]
DEFAULT_DURATION_SEC = 1 * 60


@dataclass
class TimerState:
    """In-memory timer snapshot stored in Streamlit session_state."""

    duration_sec: int
    remaining_sec: int
    timer_status: TimerStatus
    last_tick_ts: float | None


def create_default_state() -> TimerState:
    """Build the initial 25-minute idle state."""
    return TimerState(
        duration_sec=DEFAULT_DURATION_SEC,
        remaining_sec=DEFAULT_DURATION_SEC,
        timer_status="idle",
        last_tick_ts=None,
    )
