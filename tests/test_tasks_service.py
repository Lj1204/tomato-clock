from __future__ import annotations

from src.tasks import service


def test_create_toggle_delete_and_accumulate_task() -> None:
    store: list[dict] = []

    original_load = service.load_tasks
    original_save = service.save_tasks
    original_append = service.append_task
    try:
        service.load_tasks = lambda: [dict(item) for item in store]  # type: ignore[assignment]
        service.save_tasks = lambda items: store.clear() or store.extend(items)  # type: ignore[assignment]
        service.append_task = lambda task: store.append(task.to_dict())  # type: ignore[assignment]

        created = service.create_task("Read chapter 1")
        assert created is True
        assert len(store) == 1
        task_id = str(store[0]["id"])
        assert store[0]["status"] == "todo"

        service.add_pomodoro_to_task(task_id, 90)
        assert store[0]["pomodoro_count"] == 1
        assert store[0]["focus_seconds"] == 90

        service.toggle_task_status(task_id)
        assert store[0]["status"] == "done"

        service.delete_task(task_id)
        assert store == []
    finally:
        service.load_tasks = original_load  # type: ignore[assignment]
        service.save_tasks = original_save  # type: ignore[assignment]
        service.append_task = original_append  # type: ignore[assignment]
