import streamlit as st

from src.ui.stats_panel import render_stats_panel
from src.ui.tasks_panel import render_tasks_panel
from src.ui.timer_panel import render_timer_panel

st.set_page_config(page_title="Pomodoro Clock", page_icon="🍅", layout="centered")

st.markdown(
    """
    <style>
    :root {
      --bg: #fff7f4;
      --card: #fffefc;
      --text: #2e1c1a;
      --muted: #7f6662;
      --tomato: #e2492f;
      --tomato-dark: #be3119;
      --leaf: #2f8f4e;
      --line: #f2ddd6;
      --shadow: 0 10px 28px rgba(180, 77, 53, 0.10);
      --radius-xl: 18px;
      --radius-lg: 14px;
      --radius-md: 10px;
    }

    html, body, [data-testid="stAppViewContainer"] {
      background: radial-gradient(circle at 10% -20%, #ffe5dc 0%, var(--bg) 40%) no-repeat;
      color: var(--text);
      font-family: "IBM Plex Sans", "Noto Sans SC", "Source Han Sans SC", sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }

    .app-hero {
      margin-top: 0.3rem;
      margin-bottom: 0.6rem;
      background: linear-gradient(120deg, #ffede6 0%, #fff9f6 70%);
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
      padding: 1rem 1.1rem 0.9rem 1.1rem;
    }

    .app-title {
      margin: 0;
      font-size: 1.6rem;
      letter-spacing: 0.02em;
      color: var(--tomato-dark);
      font-weight: 760;
    }

    .app-subtitle {
      margin: 0.25rem 0 0 0;
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1.45;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
      border-radius: var(--radius-xl) !important;
      border: 1px solid var(--line) !important;
      background: var(--card) !important;
      box-shadow: var(--shadow) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
      padding: 0.35rem 0.5rem 0.65rem 0.5rem;
    }

    .panel-title {
      color: var(--tomato-dark);
      font-size: 1.16rem;
      font-weight: 700;
      margin-bottom: 0.15rem;
    }

    .panel-note {
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 0.3rem;
    }

    .stButton > button {
      border-radius: var(--radius-md);
      border: 1px solid #f0d1c8;
      font-weight: 620;
      transition: all .16s ease;
    }

    .stButton > button:hover {
      border-color: #e9beb1;
      transform: translateY(-1px);
    }

    .stSuccess {
      border-radius: var(--radius-md);
      border: 1px solid #caebd5;
      background: #f1fbf4;
    }

    .stInfo {
      border-radius: var(--radius-md);
      border: 1px solid #d4e6ff;
      background: #f4f9ff;
    }

    .stWarning {
      border-radius: var(--radius-md);
      border: 1px solid #f1d1b5;
      background: #fff7f1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-hero">
      <h1 class="app-title">番茄时钟</h1>
      <p class="app-subtitle">专注一件事，完成一个番茄，再向前一步。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    render_timer_panel()

with st.container(border=True):
    render_stats_panel()

with st.container(border=True):
    render_tasks_panel()
