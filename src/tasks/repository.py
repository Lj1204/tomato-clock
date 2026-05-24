from __future__ import annotations

import json
from pathlib import Path

from src.tasks.models import TaskRecord

TASKS_FILE = Path("data/tasks/tasks.json")


def _ensure_storage() -> None:
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def _read_all() -> list[dict]:
    _ensure_storage()
    text = TASKS_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return data


def _write_all(items: list[dict]) -> None:
    _ensure_storage()
    TASKS_FILE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_tasks() -> list[dict]:
    items = _read_all()
    normalized: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        task = dict(item)
        # Backward-compatible migration:
        # - completed(bool) -> status(todo|done)
        # - focus_minutes -> focus_seconds
        if "status" not in task:
            completed = bool(task.get("completed", False))
            task["status"] = "done" if completed else "todo"
        if "focus_seconds" not in task:
            minutes = int(task.get("focus_minutes", 0))
            task["focus_seconds"] = max(0, minutes) * 60
        task.setdefault("pomodoro_count", 0)
        task.setdefault("title", "")
        task.setdefault("id", "")
        task.setdefault("created_at", "")
        task.setdefault("updated_at", "")
        normalized.append(task)
    return normalized


def save_tasks(items: list[dict]) -> None:
    try:
        _write_all(items)
    except OSError as exc:
        raise RuntimeError(f"写入任务数据失败: {exc}") from exc


def append_task(task: TaskRecord) -> None:
    try:
        items = _read_all()
        items.append(task.to_dict())
        _write_all(items)
    except OSError as exc:
        raise RuntimeError(f"追加任务失败: {exc}") from exc
