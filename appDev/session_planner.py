import streamlit as st


PRACTICES = [
    "Vipasanna",
    "Non dual awakening",
    "Compassionate awakening",
    "Non sleep deep rest",
    "Custom",
]

DURATIONS = [5, 10, 15, 20, 30, 45, 60]


def init_planner_state():
    defaults = {
        "planner_practice": "Vipasanna",
        "planner_mode": "Silent",
        "planner_duration": 10,
        "planner_eeg_connected": True,
        "planner_band_connected": False,
        "session_config": None,
        "session_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def save_session_config():
    st.session_state["session_config"] = {
        "practice": st.session_state["planner_practice"],
        "mode": st.session_state["planner_mode"],
        "duration_min": st.session_state["planner_duration"],
        "guided_style": None,
        "notes": "",
        "devices": {
            "eeg": st.session_state["planner_eeg_connected"],
            "band": st.session_state["planner_band_connected"],
        },
        "started": True,
    }
    st.session_state["session_started"] = True


def render_session_planner(on_back=None):
    init_planner_state()

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
        PRACTICES,
        index=PRACTICES.index(st.session_state["planner_practice"]),
    )

    mode = st.radio(
        "Mode",
        ["Guided", "Silent"],
        horizontal=True,
        index=0 if st.session_state["planner_mode"] == "Guided" else 1,
    )

    duration = st.select_slider(
        "Duration",
        options=DURATIONS,
        value=st.session_state["planner_duration"],
        format_func=lambda value: f"{value} min",
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
        st.session_state["planner_duration"] = duration
        st.session_state["planner_eeg_connected"] = eeg_connected
        st.session_state["planner_band_connected"] = band_connected
        save_session_config()
        st.success("Session config saved.")

    st.divider()

    st.subheader("Preview")
    preview_left, preview_right = st.columns([2, 1])

    with preview_left:
        st.markdown(f"**Practice:** {practice}")
        st.markdown(f"**Mode:** {mode}")
        st.markdown(f"**Duration:** {duration} min")

    with preview_right:
        st.markdown(f"**EEG:** {'Connected' if eeg_connected else 'Not connected'}")
        st.markdown(f"**Band:** {'Connected' if band_connected else 'Not connected'}")
