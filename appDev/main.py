import streamlit as st

from app_state import go_to, init_app_state
from home_view import render_home
from library_card import init_library_state, render_library_view
from placeholder_view import render_placeholder_view
from session_planner import init_planner_state, render_session_planner
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

    current_view = st.session_state.current_view

    if current_view == "home":
        render_home(go_to)
    elif current_view == "planner":
        render_session_planner(on_back=lambda: go_to("home"))
    elif current_view == "library":
        render_library_view(on_back=lambda: go_to("home"))
    elif current_view == "repository":
        render_placeholder_view(
            "Global repository",
            "This route is reserved for shared resources and community content.",
            go_to,
        )
    else:
        go_to("home")
        st.rerun()


if __name__ == "__main__":
    main()
