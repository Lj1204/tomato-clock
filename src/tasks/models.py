from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

TaskStatus = Literal["todo", "done"]

@dataclass
class TaskRecord:
    id: str
    title: str
    status: TaskStatus
    pomodoro_count: int
    focus_seconds: int
    created_at: str
    updated_at: str

    def to_dict(self) -> dict:
        return asdict(self)
