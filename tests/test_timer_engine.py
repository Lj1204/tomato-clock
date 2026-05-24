from __future__ import annotations

from types import SimpleNamespace

from src.timer import engine


def _state(duration: int = 60) -> SimpleNamespace:
    return SimpleNamespace(
        duration_sec=duration,
        remaining_sec=duration,
        timer_status="idle",
        last_tick_ts=None,
    )


def test_start_pause_resume_reset_flow() -> None:
    state = _state(60)

    engine.start(state)
    assert state.timer_status == "running"
    assert state.last_tick_ts is not None

    engine.pause(state)
    assert state.timer_status == "paused"
    assert state.last_tick_ts is None

    engine.resume(state)
    assert state.timer_status == "running"
    assert state.last_tick_ts is not None

    engine.reset(state)
    assert state.timer_status == "idle"
    assert state.remaining_sec == state.duration_sec
    assert state.last_tick_ts is None


def test_tick_never_goes_negative() -> None:
    state = _state(10)
    state.timer_status = "running"
    state.last_tick_ts = 100.0

    original_now = engine._now
    try:
        engine._now = lambda: 1000.0  # type: ignore[assignment]
        engine.tick(state)
    finally:
        engine._now = original_now  # type: ignore[assignment]

    assert state.remaining_sec == 0
    assert state.timer_status == "idle"
