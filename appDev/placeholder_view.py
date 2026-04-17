import streamlit as st


def render_placeholder_view(title: str, message: str, go_to):
    if st.button("Back", key=f"back_{title.lower().replace(' ', '_')}"):
        go_to("home")
        st.rerun()

    st.title(title)
    st.caption(message)
    st.info("This section is intentionally left empty for the pitch demo.")
