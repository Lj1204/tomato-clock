import streamlit as st

st.set_page_config(page_title="AI Pomodoro Clock", page_icon="🍅", layout="centered")

st.title("AI 番茄时钟")
st.caption("阶段 0 占位页面：项目初始化完成后，这里将接入计时、统计与 AI 建议模块。")

with st.container(border=True):
    st.subheader("项目状态")
    st.write("- 当前阶段：Stage 0（初始化）")
    st.write("- 下一步：实现计时核心（Stage 1）")
