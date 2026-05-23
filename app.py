import streamlit as st

from src.ui.stats_panel import render_stats_panel
from src.ui.timer_panel import render_timer_panel

st.set_page_config(page_title="AI Pomodoro Clock", page_icon="🍅", layout="centered")

st.title("AI 番茄时钟")
st.caption("阶段 2：每日统计")

with st.container(border=True):
    render_timer_panel()

with st.container(border=True):
    render_stats_panel()
