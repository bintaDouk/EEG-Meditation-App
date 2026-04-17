import time

import streamlit as st


RUNTIME_KEY = "session_runtime"


def init_session_runtime(duration_seconds: int):
    now = time.time()
    session_duration_sec = duration_seconds
    st.session_state[RUNTIME_KEY] = {
        "session_duration_sec": session_duration_sec,
        "session_ends_at": now + session_duration_sec,
        "session_remaining_sec": session_duration_sec,
        "session_phase": "running",
        "session_media_started": False,
        "last_tick_timestamp": now,
    }


def get_session_runtime():
    runtime = st.session_state.get(RUNTIME_KEY)
    if not runtime:
        return None

    now = time.time()
    session_remaining = max(0, int(runtime["session_ends_at"] - now + 0.999))

    if now < runtime["session_ends_at"]:
        phase = "running"
    else:
        phase = "complete"
        session_remaining = 0

    runtime["session_remaining_sec"] = session_remaining
    runtime["session_phase"] = phase
    runtime["last_tick_timestamp"] = now

    if phase == "running":
        runtime["session_media_started"] = True

    st.session_state[RUNTIME_KEY] = runtime
    return runtime


def clear_session_runtime():
    st.session_state.pop(RUNTIME_KEY, None)
