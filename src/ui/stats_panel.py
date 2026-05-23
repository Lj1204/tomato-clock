from __future__ import annotations

import streamlit as st

from src.stats.service import get_today_stats


def render_stats_panel() -> None:
    stats = get_today_stats()

    st.subheader("今日统计")
    if stats.completed_count == 0:
        st.caption("今天还没有完成番茄钟，先开始第一个 25 分钟吧。")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric("完成次数", stats.completed_count)
    with col2:
        st.metric("专注分钟", stats.focus_minutes)
