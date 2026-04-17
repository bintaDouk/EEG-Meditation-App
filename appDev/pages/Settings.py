from utils import _css
import streamlit as st
from utils import (
    load_data,
    add_exercise,
    delete_exercise,
    reset_all_logs,
)

_css()
st.title("⚙️ Settings")

data = load_data()

# ── Add exercise ──
st.subheader("Add exercise")
new_ex = st.text_input("Name")

if st.button("Add") and new_ex:
    add_exercise(new_ex)
    st.rerun()

# ── Delete exercise ──
st.subheader("Delete exercise")

if data["exercises"]:
    ex = st.selectbox("Select", data["exercises"])

    if st.button("Delete"):
        delete_exercise(ex)
        st.rerun()

# ── Reset ──
st.subheader("Reset")

if st.button("Reset all logs"):
    reset_all_logs()
    st.rerun()