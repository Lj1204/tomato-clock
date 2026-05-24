from __future__ import annotations

import streamlit as st

from src.tasks.service import (
    create_task,
    delete_task,
    format_focus_minutes,
    get_tasks,
    toggle_task_status,
)


CURRENT_TASK_ID_KEY = "current_task_id"
CURRENT_TASK_SELECT_KEY = "current_task_id_select"
DELETE_CONFIRM_TASK_ID_KEY = "delete_confirm_task_id"
TASK_FEEDBACK_KEY = "task_feedback_message"


def ensure_task_state() -> None:
    """Initialize task-related session keys once."""
    if CURRENT_TASK_ID_KEY not in st.session_state:
        st.session_state[CURRENT_TASK_ID_KEY] = ""
    if CURRENT_TASK_SELECT_KEY not in st.session_state:
        st.session_state[CURRENT_TASK_SELECT_KEY] = ""
    if DELETE_CONFIRM_TASK_ID_KEY not in st.session_state:
        st.session_state[DELETE_CONFIRM_TASK_ID_KEY] = ""
    if TASK_FEEDBACK_KEY not in st.session_state:
        st.session_state[TASK_FEEDBACK_KEY] = ""


def set_task_feedback(message: str) -> None:
    st.session_state[TASK_FEEDBACK_KEY] = message


def _task_label(task: dict) -> str:
    status_label = "已完成任务" if str(task.get("status", "todo")) == "done" else "待办任务"
    pomodoro_count = int(task.get("pomodoro_count", 0))
    focus_minutes = format_focus_minutes(task)
    return (
        f"{task.get('title', '')} | {status_label} | "
        f"番茄投入 {pomodoro_count} 次 | 专注时长 {focus_minutes} 分钟"
    )


def _render_current_task_selector(tasks: list[dict]) -> None:
    options = [""] + [str(task.get("id", "")) for task in tasks]
    if st.session_state[CURRENT_TASK_SELECT_KEY] not in options:
        st.session_state[CURRENT_TASK_SELECT_KEY] = ""

    selected = st.selectbox(
        "当前专注任务",
        options=options,
        format_func=lambda task_id: (
            "未选择任务"
            if not task_id
            else next(
                (
                    task.get("title", "")
                    for task in tasks
                    if str(task.get("id", "")) == task_id
                ),
                "未知任务",
            )
        ),
        key=CURRENT_TASK_SELECT_KEY,
    )
    st.session_state[CURRENT_TASK_ID_KEY] = selected
    if not selected:
        st.info("未选择任务时，番茄计时仍可进行，但不会写入任务投入。")


def _render_task_group(title: str, items: list[dict]) -> None:
    st.markdown(f"**{title}**")
    if not items:
        st.caption("暂无")
        return

    for task in items:
        col1, col2, col3 = st.columns([6, 2, 2])
        task_id = str(task.get("id", ""))
        with col1:
            st.write(_task_label(task))
        with col2:
            toggle_label = "恢复任务" if str(task.get("status", "todo")) == "done" else "完成任务"
            if st.button(toggle_label, key=f"toggle_{task_id}", use_container_width=True):
                toggle_task_status(task_id)
                st.success("任务状态已更新。")
                st.rerun()
        with col3:
            if st.button("删除", key=f"delete_prepare_{task_id}", use_container_width=True):
                st.session_state[DELETE_CONFIRM_TASK_ID_KEY] = task_id
                st.rerun()


def _render_delete_confirm(tasks: list[dict]) -> None:
    confirm_id = str(st.session_state.get(DELETE_CONFIRM_TASK_ID_KEY, "")).strip()
    if not confirm_id:
        return

    task = next((item for item in tasks if str(item.get("id", "")) == confirm_id), None)
    if task is None:
        st.session_state[DELETE_CONFIRM_TASK_ID_KEY] = ""
        return

    st.warning(f"确认删除任务：{task.get('title', '')}？删除后该任务投入数据也会移除。")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("确认删除", key=f"delete_confirm_{confirm_id}", use_container_width=True):
            if st.session_state[CURRENT_TASK_ID_KEY] == confirm_id:
                st.session_state[CURRENT_TASK_ID_KEY] = ""
                st.session_state[CURRENT_TASK_SELECT_KEY] = ""
            delete_task(confirm_id)
            st.session_state[DELETE_CONFIRM_TASK_ID_KEY] = ""
            st.success("任务已删除。")
            st.rerun()
    with col2:
        if st.button("取消", key=f"delete_cancel_{confirm_id}", use_container_width=True):
            st.session_state[DELETE_CONFIRM_TASK_ID_KEY] = ""
            st.rerun()


def render_tasks_panel() -> None:
    ensure_task_state()

    st.markdown('<div class="panel-title">专注任务</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-note">任务完成与番茄完成是两件事：番茄归零只累计投入，不会自动完成任务。</div>',
        unsafe_allow_html=True,
    )

    if st.session_state[TASK_FEEDBACK_KEY]:
        st.success(st.session_state[TASK_FEEDBACK_KEY])
        st.session_state[TASK_FEEDBACK_KEY] = ""

    title = st.text_input("新增任务", placeholder="例如：完成线代第3章习题")
    if st.button("添加任务", use_container_width=True):
        if create_task(title):
            st.success("任务已添加。")
            st.rerun()
        st.warning("任务标题不能为空。")

    try:
        tasks = get_tasks()
    except RuntimeError as exc:
        st.error(str(exc))
        return

    todo_count = len([task for task in tasks if str(task.get("status", "todo")) == "todo"])
    done_count = len(tasks) - todo_count
    st.caption(f"任务总数：{len(tasks)} | 待办：{todo_count} | 已完成：{done_count}")
    _render_current_task_selector(tasks)

    if not tasks:
        st.caption("还没有任务，先添加一个专注目标吧。")
        return

    todo_tasks = [task for task in tasks if str(task.get("status", "todo")) == "todo"]
    done_tasks = [task for task in tasks if str(task.get("status", "todo")) == "done"]

    _render_task_group("待办任务", todo_tasks)
    _render_task_group("已完成任务", done_tasks)
    _render_delete_confirm(tasks)
