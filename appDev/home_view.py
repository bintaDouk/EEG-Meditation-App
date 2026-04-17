import streamlit as st

from analytics_view import render_analytics_panel


def _render_clickable_card(title: str, copy: str, href: str, placeholder: str = ""):
    placeholder_html = (
        f'<div class="placeholder">{placeholder}</div>' if placeholder else ""
    )
    st.markdown(
        f"""
        <div class="card card-clickable" onclick="window.location.href='{href}'">
            <div class="card-title">{title}</div>
            <div class="card-copy">{copy}</div>
            {placeholder_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home(go_to):
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Open Source Meditation</div>
            <div class="hero-title">A quieter way to begin</div>
            <div class="hero-copy">
                Choose how you want to practice, begin a new session, or return to your
                meditation history when those views are ready.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    start_col, submit_col, repository_col = st.columns(3, gap="large")

    with start_col:
        _render_clickable_card(
            "Begin meditation",
            "Start a new practice with a calm session planner and device preview.",
            "?view=planner",
        )

    with submit_col:
        _render_clickable_card(
            "Submit recorded session",
            "Upload a completed session from another workflow.",
            "?view=submit",
        )

    with repository_col:
        _render_clickable_card(
            "Global repository",
            "Shared knowledge and community resources can live here later.",
            "?view=repository",
        )

    st.markdown("## Your analytics")
    st.caption("A calm snapshot of your practice so far.")
    render_analytics_panel()
