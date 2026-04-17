import streamlit as st


def init_app_state():
    requested_view = st.query_params.get("view")
    if requested_view:
        st.session_state.current_view = requested_view

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"


def go_to(view_name: str):
    st.session_state.current_view = view_name
    if view_name == "home":
        st.query_params.clear()
    else:
        st.query_params["view"] = view_name
