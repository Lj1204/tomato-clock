from __future__ import annotations

import time

import streamlit as st

from src.stats.service import record_completed_session
from src.tasks.service import add_pomodoro_to_task
from src.ui.tasks_panel import set_task_feedback
from src.timer import engine
from src.timer.formatter import format_mmss
from src.timer.session import ensure_timer_state


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
        record_completed_session(st.session_state.duration_sec)
        current_task_id = str(st.session_state.get("current_task_id", "")).strip()
        if current_task_id:
            # Link one completed pomodoro to the selected task exactly once.
            add_pomodoro_to_task(current_task_id, st.session_state.duration_sec)
            set_task_feedback("已为当前任务累计 1 个番茄投入。")

    st.subheader("Pomodoro Timer")
    st.markdown(f"## {format_mmss(st.session_state.remaining_sec)}")
    st.caption(f"Status: {st.session_state.timer_status}")

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
