from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class SessionRecord:
    id: str
    started_at: str
    ended_at: str
    duration_sec: int
    completed: bool
    date: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DailyStats:
    date: str
    completed_count: int
    focus_minutes: int
