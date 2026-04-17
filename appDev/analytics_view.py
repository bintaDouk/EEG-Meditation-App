from datetime import datetime
from html import escape
from textwrap import dedent

import streamlit as st

from utils import _css, load_data, radar_plot


def _parse_session_timestamp(session: dict):
    raw_timestamp = session.get("ts", "")
    try:
        parsed = datetime.fromisoformat(raw_timestamp)
    except (TypeError, ValueError):
        return None, str(raw_timestamp)

    return parsed, parsed.strftime("%b %d, %H:%M")


def _format_session_duration(session: dict) -> str:
    if "duration_seconds" in session:
        seconds = session["duration_seconds"]
        if seconds < 60:
            return f"{seconds} sec"
        return f"{seconds // 60} min"

    duration_min = session.get("duration_min")
    if duration_min is None:
        return "Duration unavailable"
    return f"{duration_min} min"


def _sorted_sessions(data: dict) -> list[dict]:
    sortable_sessions = []
    for session in data.get("sessions", []):
        parsed, label = _parse_session_timestamp(session)
        sortable_sessions.append((parsed or datetime.min, label, session))

    sortable_sessions.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            **session,
            "_display_time": label,
        }
        for _, label, session in sortable_sessions
    ]


def _render_session_history_panel(data: dict):
    sessions = _sorted_sessions(data)

    if not sessions:
        st.markdown(
            dedent(
                """
                <div class="analytics-history-card">
                    <div class="analytics-history-title">Session history</div>
                    <div class="analytics-history-empty">
                        Your latest sessions will appear here once they are logged.
                    </div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True,
        )
        return

    rows = []
    for session in sessions:
        exercise = escape(str(session.get("exercise", "Unknown practice")))
        timestamp = escape(str(session["_display_time"]))
        duration = escape(_format_session_duration(session))
        rows.append(
            dedent(
                f"""
                <div class="analytics-history-row">
                    <div class="analytics-history-row-top">
                        <span class="analytics-history-exercise">{exercise}</span>
                        <span class="analytics-history-duration">{duration}</span>
                    </div>
                    <div class="analytics-history-time">{timestamp}</div>
                </div>
                """
            ).strip()
        )

    st.markdown(
        dedent(
            f"""
            <div class="analytics-history-card">
                <div class="analytics-history-title">Session history</div>
                <div class="analytics-history-scroll">{''.join(rows)}</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_analytics_panel(go_to=None):
    _css()

    data = load_data()

    radar_col, history_col = st.columns([1.62, 0.62], gap="medium")

    with radar_col:
        st.markdown(
            """
            <div class="analytics-panel-head">
                <div class="analytics-panel-title">Practice map</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not data["averages"]:
            st.info("No sessions logged yet.")
        else:
            fig = radar_plot(data["exercises"], data["averages"])
            fig.set_size_inches(5.95, 5.95)
            st.pyplot(fig)
        if go_to is not None and st.button("Logbook", key="analytics_logbook_button"):
            go_to("logbook")
            st.rerun()

    with history_col:
        _render_session_history_panel(data)

    st.subheader("Overall averages")

    if not data["averages"]:
        st.info("No data available yet.")
        return

    for exercise in data["exercises"]:
        avg = data["averages"].get(exercise)
        if avg is None:
            continue

        count = data["counts"].get(exercise, 0)
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{exercise}**")
        with col2:
            st.markdown(f"`{avg:.2f}`")
        with col3:
            st.markdown(f"_{count} session{'s' if count != 1 else ''}_")
