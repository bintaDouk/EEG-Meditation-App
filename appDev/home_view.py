import streamlit as st

from analytics_view import render_analytics_panel
from begin_meditation_card import render_begin_meditation_card
from global_repository_card import render_global_repository_card
from library_card import render_library_card


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

    start_col, library_col, repository_col = st.columns(3, gap="large")

    with start_col:
        render_begin_meditation_card()

    with library_col:
        render_library_card()

    with repository_col:
        render_global_repository_card()

    st.markdown("## Your analytics")
    st.caption("A calm snapshot of your practice so far.")
    render_analytics_panel()
