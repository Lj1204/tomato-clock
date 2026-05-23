from __future__ import annotations

import json
from pathlib import Path

from src.stats.models import SessionRecord

SESSIONS_FILE = Path("data/sessions/sessions.json")


def _ensure_storage() -> None:
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SESSIONS_FILE.exists():
        SESSIONS_FILE.write_text("[]", encoding="utf-8")


def _read_all() -> list[dict]:
    _ensure_storage()
    text = SESSIONS_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return data


def append_session(record: SessionRecord) -> None:
    data = _read_all()
    data.append(record.to_dict())
    SESSIONS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_sessions_by_date(date_str: str) -> list[dict]:
    data = _read_all()
    return [item for item in data if item.get("date") == date_str]
