import streamlit as st

from utils import get_available_exercises
from session_runtime import RUNTIME_KEY, init_session_runtime

DEMO_DURATION_SECONDS = 30
DURATION_OPTIONS = [DEMO_DURATION_SECONDS] + [minute * 60 for minute in range(1, 61)]


def _format_duration_label(duration_seconds: int) -> str:
    if duration_seconds < 60:
        return f"{duration_seconds} sec"
    minutes = duration_seconds // 60
    return f"{minutes} min"


def init_planner_state():
    practices = get_available_exercises()
    default_practice = practices[0] if practices else "Breathing Focus"
    defaults = {
        "planner_practice": default_practice,
        "planner_mode": "Silent",
        "planner_duration_seconds": DEMO_DURATION_SECONDS,
        "planner_eeg_connected": True,
        "planner_band_connected": False,
        "session_config": None,
        "session_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def save_session_config():
    duration_seconds = st.session_state["planner_duration_seconds"]
    st.session_state["session_config"] = {
        "practice": st.session_state["planner_practice"],
        "mode": st.session_state["planner_mode"],
        "duration_seconds": duration_seconds,
        "duration_label": _format_duration_label(duration_seconds),
        "guided_style": None,
        "notes": "",
        "devices": {
            "eeg": st.session_state["planner_eeg_connected"],
            "band": st.session_state["planner_band_connected"],
        },
        "started": True,
    }
    st.session_state["session_started"] = True


def render_session_planner(on_back=None, on_start=None):
    init_planner_state()
    practices = get_available_exercises()
    if not practices:
        practices = ["Breathing Focus"]
    if st.session_state["planner_practice"] not in practices:
        st.session_state["planner_practice"] = practices[0]

    # If a live session runtime exists, the planner should never render again.
    if st.session_state.get(RUNTIME_KEY):
        if on_start is not None:
            on_start()
        st.rerun()

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.title("Open Source Meditation")
        st.caption("a quiet place to begin your practice")
    with top_right:
        if on_back is not None and st.button("Back", use_container_width=True):
            on_back()
            st.rerun()

    practice = st.selectbox(
        "Meditation type",
        practices,
        index=practices.index(st.session_state["planner_practice"]),
    )

    mode = st.radio(
        "Mode",
        ["Guided", "Silent"],
        horizontal=True,
        index=0 if st.session_state["planner_mode"] == "Guided" else 1,
    )

    duration = st.select_slider(
        "Duration",
        options=DURATION_OPTIONS,
        value=st.session_state["planner_duration_seconds"],
        format_func=_format_duration_label,
    )

    st.markdown("**Connected devices**")
    device_left, device_right = st.columns(2)
    with device_left:
        eeg_connected = st.toggle(
            "EEG connected",
            value=st.session_state["planner_eeg_connected"],
        )
    with device_right:
        band_connected = st.toggle(
            "Band connected",
            value=st.session_state["planner_band_connected"],
        )

    st.markdown(
        """
        <div class="quote-card">
            "Meditation is the discovery that the point of life is always arrived at
            in the immediate moment."
            <span class="quote-author">Alan Watts</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start session", use_container_width=True, type="primary"):
        st.session_state["planner_practice"] = practice
        st.session_state["planner_mode"] = mode
        st.session_state["planner_duration_seconds"] = duration
        st.session_state["planner_eeg_connected"] = eeg_connected
        st.session_state["planner_band_connected"] = band_connected
        save_session_config()
        init_session_runtime(duration)
        if on_start is not None:
            on_start()
        st.rerun()

    st.divider()

    st.subheader("Preview")
    preview_left, preview_right = st.columns([2, 1])

    with preview_left:
        st.markdown(f"**Practice:** {practice}")
        st.markdown(f"**Mode:** {mode}")
        st.markdown(f"**Duration:** {_format_duration_label(duration)}")

    with preview_right:
        st.markdown(f"**EEG:** {'Connected' if eeg_connected else 'Not connected'}")
        st.markdown(f"**Band:** {'Connected' if band_connected else 'Not connected'}")
