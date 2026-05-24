from __future__ import annotations

from src.stats import service


def test_get_today_stats_aggregates_completed_sessions() -> None:
    original_today = service.today_str
    original_loader = service.load_sessions_by_date
    try:
        service.today_str = lambda: "2026-05-24"  # type: ignore[assignment]
        service.load_sessions_by_date = lambda _date: [  # type: ignore[assignment]
            {"completed": True, "duration_sec": 1500},
            {"completed": True, "duration_sec": 600},
            {"completed": False, "duration_sec": 1500},
        ]
        stats = service.get_today_stats()
    finally:
        service.today_str = original_today  # type: ignore[assignment]
        service.load_sessions_by_date = original_loader  # type: ignore[assignment]

    assert stats.date == "2026-05-24"
    assert stats.completed_count == 2
    assert stats.focus_minutes == 35
