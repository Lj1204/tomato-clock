import streamlit as st

from src.ui.stats_panel import render_stats_panel
from src.ui.tasks_panel import render_tasks_panel
from src.ui.timer_panel import render_timer_panel

st.set_page_config(page_title="Pomodoro Clock", page_icon="🍅", layout="centered")

st.title("番茄时钟")
st.caption("阶段 3：计时 + 每日统计 + 专注任务")

with st.container(border=True):
    render_timer_panel()

with st.container(border=True):
    render_stats_panel()

with st.container(border=True):
    render_tasks_panel()
