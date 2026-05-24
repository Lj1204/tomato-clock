# Pomodoro Clock

一个基于 Python + Streamlit 的本地番茄时钟应用，支持倒计时、每日统计和专注任务联动。

## 项目说明
- 这是我的第一个 Vibe Coding 项目。
- 本项目主要使用的 AI 模型：`gpt-5.3-codex`。
- 累计花费$0.19，共调用 236 次 API。

## 功能
- 计时器：开始、暂停、继续、重置
- 每日统计：完成番茄次数、专注分钟
- 专注任务：新增、完成/恢复、删除、与番茄完成事件联动累计

## 环境要求
- Python 3.10+
- Windows / macOS / Linux

## 快速开始
1. 创建并激活虚拟环境
2. 安装依赖
3. 启动应用

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 测试
```bash
python -m pytest -q
```

## 数据文件
- `data/sessions/sessions.json`：番茄完成记录
- `data/tasks/tasks.json`：任务数据

## 常见错误
- `写入专注记录失败` / `写入任务数据失败`：
  - 通常是文件被占用或目录权限不足，关闭占用进程后重试。
- `No module named pytest`：
  - 运行 `python -m pip install -r requirements.txt` 重新安装依赖。
- 页面按钮点击无反应：
  - 确认是否在同一个虚拟环境启动：`.venv\Scripts\python.exe -m streamlit run app.py`。
