import streamlit as st
from utils import _css, load_data, radar_plot

# MUST be first Streamlit command
st.set_page_config(page_title="Meditation Radar", layout="wide", page_icon="🧘")

# ── Radar plot ────────────────────────────
def Dashboard():
    _css()
    data = load_data()

    st.title("Open Source Meditation App")
    st.subheader("Dashboard")

    # ── Radar (smaller & centered) ─────────────────────
    if not data["averages"]:
        st.info("No sessions logged yet.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            fig = radar_plot(data["exercises"], data["averages"])
            fig.set_size_inches(4.5, 4.5)  # 👈 smaller
            st.pyplot(fig)

# ── Averages + sessions ────────────────────────────
def SessionStats():
    _css()
    data = load_data()
    
    st.subheader("Overall averages")

    if not data["averages"]:
        st.info("No data available yet.")
    else:
        for ex in data["exercises"]:
            avg = data["averages"].get(ex)
            if avg is None:
                continue

            n = data["counts"].get(ex, 0)

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown(f"**{ex}**")

            with col2:
                st.markdown(f"`{avg:.2f}`")

            with col3:
                st.markdown(f"_{n} session{'s' if n != 1 else ''}_")


def main():
    Dashboard()
    SessionStats()


if __name__ == "__main__":
    main()