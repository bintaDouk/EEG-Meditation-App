from utils import _css
import streamlit as st
from utils import load_data, log_session, score_from_eeg, radar_plot

_css()
st.title("🧘 Session Log")

data = load_data()

# ── Log session ──
exercise = st.selectbox("Exercise", data["exercises"])
duration = st.slider("Duration (min)", 1, 90, 20)

if st.button("Complete session"):
    score = score_from_eeg(exercise, duration)
    prev_avg, new_avg = log_session(exercise, score, duration)

    st.success(f"Score: {score:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar_plot(data["exercises"], prev_avg))
    with col2:
        st.pyplot(radar_plot(data["exercises"], new_avg))

# ── Session history ──
st.subheader("History")

for s in reversed(data["sessions"][-30:]):
    st.write(f"{s['exercise']} | {s['score']:.2f}")