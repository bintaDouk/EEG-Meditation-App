import streamlit as st

from utils import _css, load_data, radar_plot


def render_analytics_panel():
    _css()

    data = load_data()

    if not data["averages"]:
        st.info("No sessions logged yet.")
    else:
        left, middle, right = st.columns([1, 2, 1])
        with middle:
            fig = radar_plot(data["exercises"], data["averages"])
            fig.set_size_inches(4.5, 4.5)
            st.pyplot(fig)

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
