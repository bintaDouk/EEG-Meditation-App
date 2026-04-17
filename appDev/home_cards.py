import streamlit as st


def render_card(title: str, copy: str, route_id: str):
    card_html = (
        f'<a class="home-card" href="?view={route_id}" target="_self">'
        f'<span class="home-card-title">{title}</span>'
        f'<span class="home-card-copy">{copy}</span>'
        f"</a>"
    )
    st.markdown(card_html, unsafe_allow_html=True)
