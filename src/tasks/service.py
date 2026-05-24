from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from typing import Any

from src.tasks.models import TaskRecord
from src.tasks.repository import append_task, load_tasks, save_tasks


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def get_tasks() -> list[dict]:
    return load_tasks()


def create_task(title: str) -> bool:
    clean_title = title.strip()
    if not clean_title:
        return False

    now = _now_iso()
    task = TaskRecord(
        id=str(uuid4()),
        title=clean_title,
        status="todo",
        pomodoro_count=0,
        focus_seconds=0,
        created_at=now,
        updated_at=now,
    )
    append_task(task)
    return True


def toggle_task_status(task_id: str) -> None:
    items = load_tasks()
    changed = False
    now = _now_iso()
    for task in items:
        if task.get("id") == task_id:
            current_status = str(task.get("status", "todo"))
            task["status"] = "todo" if current_status == "done" else "done"
            task["updated_at"] = now
            changed = True
            break
    if changed:
        save_tasks(items)


def delete_task(task_id: str) -> None:
    items = load_tasks()
    filtered = [task for task in items if task.get("id") != task_id]
    if len(filtered) != len(items):
        save_tasks(filtered)


def add_pomodoro_to_task(task_id: str, duration_sec: int) -> None:
    items = load_tasks()
    changed = False
    now = _now_iso()
    focus_seconds = max(0, int(duration_sec))
    for task in items:
        if task.get("id") == task_id:
            task["pomodoro_count"] = int(task.get("pomodoro_count", 0)) + 1
            task["focus_seconds"] = int(task.get("focus_seconds", 0)) + focus_seconds
            task["updated_at"] = now
            changed = True
            break
    if changed:
        save_tasks(items)


def format_focus_minutes(task: dict[str, Any]) -> int:
    focus_seconds = int(task.get("focus_seconds", 0))
    return max(0, focus_seconds) // 60
