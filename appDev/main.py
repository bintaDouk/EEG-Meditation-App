import streamlit as st

from app_state import go_to, init_app_state
from home_view import render_home
from library_card import init_library_state, render_library_view
from logbook_view import render_logbook_view
from repository_view import init_repository_state, render_repository_view
from session_planner import init_planner_state, render_session_planner
from session_runtime import RUNTIME_KEY
from session_run_view import render_session_run_view
from ui_styles import render_app_styles


def main():
    st.set_page_config(
        page_title="Open Source Meditation",
        page_icon="OM",
        layout="centered",
    )

    render_app_styles()
    init_app_state()
    init_planner_state()
    init_library_state()
    init_repository_state()

    # A live runtime session should always take over the app before any
    # normal page routing happens.
    if st.session_state.get(RUNTIME_KEY):
        st.session_state.current_view = "session_run"
        st.query_params["view"] = "session_run"
        render_session_run_view(go_to)
        st.stop()

    current_view = st.session_state.current_view

    if current_view == "home":
        render_home(go_to)
        st.stop()
    elif current_view == "planner":
        render_session_planner(
            on_back=lambda: go_to("home"),
            on_start=lambda: go_to("session_run"),
        )
        st.stop()
    elif current_view == "library":
        render_library_view(on_back=lambda: go_to("home"))
        st.stop()
    elif current_view == "logbook":
        render_logbook_view(on_back=lambda: go_to("home"))
        st.stop()
    elif current_view == "session_run":
        render_session_run_view(go_to)
        st.stop()
    elif current_view == "repository":
        render_repository_view(on_back=lambda: go_to("home"))
        st.stop()
    else:
        go_to("home")
        st.rerun()


if __name__ == "__main__":
    main()
