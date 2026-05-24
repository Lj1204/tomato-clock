from __future__ import annotations

import streamlit as st

from src.stats.service import get_today_stats


def render_stats_panel() -> None:
    stats = get_today_stats()
    target_pomodoros = 4
    progress = min(1.0, stats.completed_count / target_pomodoros) if target_pomodoros > 0 else 0.0

    st.markdown('<div class="panel-title">今日统计</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-note">用可见进度，稳住今天的专注节奏。</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("完成番茄", stats.completed_count)
    with col2:
        st.metric("专注分钟", stats.focus_minutes)

    st.caption(f"今日目标：{target_pomodoros} 个番茄")
    st.progress(progress)

    if stats.completed_count == 0:
        st.info("先种下今天的第一个番茄目标，计时开始后统计会自动累积。")
