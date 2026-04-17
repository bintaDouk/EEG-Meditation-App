from datetime import datetime

import streamlit as st

from app_state import go_to
from library_card import _set_library_page
from utils import load_data


def _parse_timestamp(raw_timestamp: str | None):
    if not raw_timestamp:
        return None, "Unknown time"
    try:
        parsed = datetime.fromisoformat(raw_timestamp)
    except (TypeError, ValueError):
        return None, str(raw_timestamp)
    return parsed, parsed.strftime("%b %d, %Y • %H:%M")


def _logbook_entries() -> list[dict]:
    data = load_data()
    entries = []
    for index, session in enumerate(data.get("sessions", [])):
        if session.get("journal_grade") is None and not session.get("journal_note"):
            continue
        parsed, label = _parse_timestamp(session.get("ts"))
        entries.append(
            {
                **session,
                "_entry_id": f"logbook_{index}",
                "_parsed_time": parsed or datetime.min,
                "_display_time": label,
            }
        )

    entries.sort(key=lambda item: item["_parsed_time"], reverse=True)
    return entries


def _open_exercise_page(exercise: str):
    _set_library_page("detail", exercise)
    go_to("library")
    st.rerun()


def render_logbook_view(on_back=None):
    st.title("Logbook")
    st.caption("Browse your reflections from newest to oldest and open any entry to read it in full.")

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.empty()
    with top_right:
        if on_back is not None and st.button("Back", use_container_width=True):
            on_back()
            st.rerun()

    entries = _logbook_entries()
    if not entries:
        st.info("Your logbook will appear here after you save notes at the end of a session.")
        return

    if st.session_state.get("selected_logbook_entry") not in {
        entry["_entry_id"] for entry in entries
    }:
        st.session_state["selected_logbook_entry"] = entries[0]["_entry_id"]

    list_col, detail_col = st.columns([1.25, 1.75], gap="large")

    with list_col:
        st.subheader("Entries")
        for entry in entries:
            label = f"{entry['_display_time']}\n{entry.get('exercise', 'Unknown practice')}"
            button_type = (
                "primary"
                if st.session_state.get("selected_logbook_entry") == entry["_entry_id"]
                else "secondary"
            )
            if st.button(
                label,
                key=entry["_entry_id"],
                use_container_width=True,
                type=button_type,
            ):
                st.session_state["selected_logbook_entry"] = entry["_entry_id"]
                st.rerun()

    selected_entry = next(
        entry
        for entry in entries
        if entry["_entry_id"] == st.session_state["selected_logbook_entry"]
    )

    with detail_col:
        st.subheader(selected_entry.get("exercise", "Unknown practice"))
        meta_parts = [selected_entry["_display_time"]]
        duration_min = selected_entry.get("duration_min")
        if duration_min is not None:
            meta_parts.append(f"{duration_min} min")
        st.caption(" • ".join(meta_parts))

        grade_left, grade_right = st.columns(2)
        with grade_left:
            journal_grade = selected_entry.get("journal_grade")
            st.metric(
                "Self-grade",
                f"{journal_grade}/10" if journal_grade is not None else "N/A",
            )
        with grade_right:
            score = selected_entry.get("score")
            st.metric(
                "Computed score",
                f"{score:.2f}" if score is not None else "N/A",
            )

        st.markdown("**Your note**")
        note = selected_entry.get("journal_note", "").strip()
        if note:
            st.write(note)
        else:
            st.write("_No note written for this session._")

        if st.button("Open exercise page", use_container_width=True, type="primary"):
            _open_exercise_page(selected_entry.get("exercise", ""))
