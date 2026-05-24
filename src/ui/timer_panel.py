from __future__ import annotations

import time

import streamlit as st

from src.stats.service import record_completed_session
from src.tasks.service import add_pomodoro_to_task
from src.ui.tasks_panel import set_task_feedback
from src.timer import engine
from src.timer.formatter import format_mmss
from src.timer.session import ensure_timer_state


def _status_label(status: str) -> str:
    return {
        "idle": "待开始",
        "running": "专注中",
        "paused": "已暂停",
    }.get(status, status)


def _status_tone(status: str) -> str:
    return {
        "idle": "#7f6662",
        "running": "#2f8f4e",
        "paused": "#c07f2a",
    }.get(status, "#7f6662")


def _progress_rate(remaining_sec: int, duration_sec: int) -> float:
    if duration_sec <= 0:
        return 0.0
    done = max(0, duration_sec - remaining_sec)
    return min(1.0, done / duration_sec)


def render_timer_panel() -> None:
    # Ensure timer state keys exist before any render/action logic.
    ensure_timer_state(st.session_state)

    prev_status = st.session_state.timer_status
    prev_remaining = st.session_state.remaining_sec

    engine.tick(st.session_state)

    # Record exactly once when a running timer reaches zero in this rerun.
    if (
        prev_status == "running"
        and st.session_state.timer_status == "idle"
        and prev_remaining > 0
        and st.session_state.remaining_sec == 0
    ):
        try:
            record_completed_session(st.session_state.duration_sec)
            current_task_id = str(st.session_state.get("current_task_id", "")).strip()
            if current_task_id:
                # Link one completed pomodoro to the selected task exactly once.
                add_pomodoro_to_task(current_task_id, st.session_state.duration_sec)
                set_task_feedback("已为当前任务累计 1 个番茄投入。")
            else:
                set_task_feedback("本次番茄已计入今日统计。")
        except RuntimeError as exc:
            st.error(str(exc))

    status = st.session_state.timer_status
    remaining = int(st.session_state.remaining_sec)
    duration = int(st.session_state.duration_sec)
    progress = _progress_rate(remaining, duration)
    status_text = _status_label(status)
    status_color = _status_tone(status)

    st.markdown('<div class="panel-title">专注计时</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-note">完成一个番茄，让注意力留在当下。</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            border:1px solid #f2ddd6;
            border-radius:14px;
            padding:0.85rem 0.9rem 0.9rem 0.9rem;
            background:linear-gradient(120deg,#fff5f1 0%,#fffefb 70%);
            margin-bottom:0.55rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
            <div style="font-size:2.2rem;font-weight:780;line-height:1;color:#be3119;">
              {format_mmss(remaining)}
            </div>
            <div style="
              font-size:0.85rem;
              color:{status_color};
              border:1px solid #f0d1c8;
              border-radius:999px;
              padding:0.24rem 0.62rem;
              background:#fff;">
              {status_text}
            </div>
          </div>
          <div style="margin-top:0.7rem;">
            <div style="height:8px;background:#f4e3dd;border-radius:999px;overflow:hidden;">
              <div style="height:8px;width:{progress * 100:.1f}%;background:#e2492f;border-radius:999px;"></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # Left button toggles between start/resume/pause based on state.
        if st.session_state.timer_status in ("idle", "paused"):
            label = "开始" if st.session_state.timer_status == "idle" else "继续"
            if st.button(label, use_container_width=True):
                if st.session_state.timer_status == "idle":
                    engine.start(st.session_state)
                else:
                    engine.resume(st.session_state)
                st.rerun()
        else:
            if st.button("暂停", use_container_width=True):
                engine.pause(st.session_state)
                st.rerun()

    with col2:
        if st.button("重置", use_container_width=True):
            engine.reset(st.session_state)
            st.rerun()

    if st.session_state.timer_status == "running":
        # Streamlit is event-driven; rerun every second to refresh countdown UI.
        time.sleep(1)
        st.rerun()
