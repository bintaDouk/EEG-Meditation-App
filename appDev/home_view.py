import streamlit as st

from analytics_view import render_analytics_panel


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
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Begin meditation</div>
                <div class="card-copy">
                    Start a new practice with a calm session planner and device preview.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open planner", use_container_width=True, key="home_begin"):
            go_to("planner")
            st.rerun()

    with submit_col:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Submit recorded session</div>
                <div class="card-copy">
                    Upload a completed session from another workflow.
                </div>
                <div class="placeholder">Empty for the pitch.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open submit", use_container_width=True, key="home_submit"):
            go_to("submit")
            st.rerun()

    with repository_col:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Global repository</div>
                <div class="card-copy">
                    Shared knowledge and community resources can live here later.
                </div>
                <div class="placeholder">Empty for the pitch.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open repository", use_container_width=True, key="home_repository"):
            go_to("repository")
            st.rerun()

    st.markdown("## Your analytics")
    st.caption("A calm snapshot of your practice so far.")
    render_analytics_panel()
