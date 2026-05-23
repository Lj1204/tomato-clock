from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.stats.models import DailyStats, SessionRecord
from src.stats.repository import append_session, load_sessions_by_date


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def record_completed_session(duration_sec: int) -> None:
    now = datetime.now()
    ended = now.isoformat(timespec="seconds")
    started = (now.timestamp() - duration_sec)
    started_iso = datetime.fromtimestamp(started).isoformat(timespec="seconds")

    record = SessionRecord(
        id=str(uuid4()),
        started_at=started_iso,
        ended_at=ended,
        duration_sec=duration_sec,
        completed=True,
        date=today_str(),
    )
    append_session(record)


def get_today_stats() -> DailyStats:
    day = today_str()
    sessions = load_sessions_by_date(day)
    completed = [item for item in sessions if item.get("completed")]
    focus_minutes = sum(int(item.get("duration_sec", 0)) for item in completed) // 60
    return DailyStats(
        date=day,
        completed_count=len(completed),
        focus_minutes=focus_minutes,
    )
