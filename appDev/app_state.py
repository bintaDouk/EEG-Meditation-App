import streamlit as st


def init_app_state():
    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"


def go_to(view_name: str):
    st.session_state.current_view = view_name
