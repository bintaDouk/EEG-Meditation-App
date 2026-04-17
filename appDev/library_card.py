from datetime import datetime

import matplotlib.pyplot as plt
import streamlit as st

from home_cards import render_card
from utils import add_exercise, delete_exercise, get_exercise_categories, get_exercise_details, load_data


ROUTE_ID = "library"
FEATURED_EXERCISE_LIMIT = 5


POWER_BAND_FREQUENCIES = list(range(1, 46))
POWER_BAND_SERIES = {
    "session 3": [
        -94.2, -99.8, -103.0, -110.2, -110.6, -114.2, -114.5, -117.1, -114.0,
        -113.2, -111.8, -115.0, -118.0, -119.6, -120.0, -120.5, -113.2, -121.0,
        -121.1, -121.3, -121.6, -122.5, -123.6, -124.8, -125.5, -125.8, -126.2,
        -126.5, -126.8, -127.0, -127.4, -127.5, -127.7, -128.2, -128.3, -128.1,
        -128.5, -128.7, -128.6, -128.4, -128.5, -128.6, -128.2, -128.3, -127.8,
    ],
    "session 2": [
        -107.3, -111.4, -114.0, -115.5, -116.8, -117.8, -118.5, -117.5, -114.4,
        -114.0, -111.3, -114.8, -117.7, -119.2, -119.8, -120.3, -113.6, -120.9,
        -120.8, -121.0, -120.8, -121.6, -123.2, -123.9, -124.5, -124.6, -125.0,
        -125.5, -125.4, -125.7, -125.5, -125.8, -125.7, -126.4, -126.4, -126.7,
        -126.6, -126.9, -126.6, -126.8, -126.5, -126.8, -126.1, -126.0, -125.4,
    ],
    "session 1": [
        -105.0, -109.6, -112.2, -115.0, -117.0, -117.9, -118.8, -118.4, -114.0,
        -110.7, -109.8, -114.5, -118.5, -120.4, -121.0, -121.4, -116.2, -121.1,
        -121.0, -121.1, -121.2, -122.8, -124.4, -125.2, -125.9, -126.1, -126.7,
        -126.9, -127.3, -127.4, -127.8, -128.2, -128.7, -128.8, -129.2, -129.4,
        -129.7, -129.8, -130.0, -130.2, -130.1, -130.3, -130.4, -130.7, -130.6,
    ],
}
POWER_BAND_EXERCISE_SERIES = {
    "Loving-kindness": [
        ("session 2", POWER_BAND_SERIES["session 3"]),
        ("session 1", POWER_BAND_SERIES["session 2"]),
        ("session 3", POWER_BAND_SERIES["session 1"]),
    ],
    "Tibetan Relaxing": [
        ("session 2", [
            -108.2, -111.4, -113.3, -114.5, -115.0, -116.7, -117.1, -116.6, -110.0,
            -110.0, -109.7, -115.8, -117.8, -119.3, -120.0, -120.4, -113.0, -121.0,
            -121.2, -121.6, -121.6, -123.8, -124.9, -125.5, -125.9, -126.0, -126.5,
            -126.7, -126.9, -127.2, -127.0, -127.4, -127.5, -127.8, -128.2, -128.1,
            -128.5, -128.5, -128.9, -128.8, -128.6, -129.0, -129.2, -129.1, -129.2,
        ]),
        ("session 1", [
            -100.0, -110.6, -113.0, -114.0, -115.8, -116.6, -117.0, -114.9, -111.4,
            -111.6, -110.0, -115.6, -118.3, -119.8, -120.3, -120.8, -113.4, -121.3,
            -121.6, -121.7, -122.1, -123.6, -124.9, -125.6, -126.1, -126.4, -126.6,
            -127.1, -127.3, -127.3, -127.7, -128.1, -128.2, -128.3, -128.6, -128.7,
            -128.7, -129.0, -129.0, -129.2, -129.1, -129.2, -129.4, -129.3, -129.6,
        ]),
    ],
    "Breathing Focus": [
        ("session 2", [
            -108.2, -111.4, -113.3, -114.5, -115.0, -116.7, -117.1, -116.6, -110.0,
            -110.0, -109.7, -115.8, -117.8, -119.3, -120.0, -120.4, -113.0, -121.0,
            -121.2, -121.6, -121.6, -123.8, -124.9, -125.5, -125.9, -126.0, -126.5,
            -126.7, -126.9, -127.2, -127.0, -127.4, -127.5, -127.8, -128.2, -128.1,
            -128.5, -128.5, -128.9, -128.8, -128.6, -129.0, -129.2, -129.1, -129.2,
        ]),
        ("session 1", [
            -100.0, -110.6, -113.0, -114.0, -115.8, -116.6, -117.0, -114.9, -111.4,
            -111.6, -110.0, -115.6, -118.3, -119.8, -120.3, -120.8, -113.4, -121.3,
            -121.6, -121.7, -122.1, -123.6, -124.9, -125.6, -126.1, -126.4, -126.6,
            -127.1, -127.3, -127.3, -127.7, -128.1, -128.2, -128.3, -128.6, -128.7,
            -128.7, -129.0, -129.0, -129.2, -129.1, -129.2, -129.4, -129.3, -129.6,
        ]),
    ],
    "Body Scan": [
        ("session 2", [
            -108.2, -111.4, -113.3, -114.5, -115.0, -116.7, -117.1, -116.6, -110.0,
            -110.0, -109.7, -115.8, -117.8, -119.3, -120.0, -120.4, -113.0, -121.0,
            -121.2, -121.6, -121.6, -123.8, -124.9, -125.5, -125.9, -126.0, -126.5,
            -126.7, -126.9, -127.2, -127.0, -127.4, -127.5, -127.8, -128.2, -128.1,
            -128.5, -128.5, -128.9, -128.8, -128.6, -129.0, -129.2, -129.1, -129.2,
        ]),
        ("session 1", [
            -100.0, -110.6, -113.0, -114.0, -115.8, -116.6, -117.0, -114.9, -111.4,
            -111.6, -110.0, -115.6, -118.3, -119.8, -120.3, -120.8, -113.4, -121.3,
            -121.6, -121.7, -122.1, -123.6, -124.9, -125.6, -126.1, -126.4, -126.6,
            -127.1, -127.3, -127.3, -127.7, -128.1, -128.2, -128.3, -128.6, -128.7,
            -128.7, -129.0, -129.0, -129.2, -129.1, -129.2, -129.4, -129.3, -129.6,
        ]),
    ],
    "Visualization": [
        ("session 1", [
            -97.6, -103.3, -104.8, -106.1, -106.4, -108.8, -109.6, -110.3, -110.7,
            -110.6, -105.6, -106.1, -110.7, -112.3, -113.0, -114.2, -114.2, -113.9,
            -111.4, -114.9, -115.0, -115.1, -115.0, -115.6, -116.5, -116.6, -117.1,
            -117.3, -117.6, -118.0, -118.6, -118.5, -118.9, -119.0, -118.9, -118.9,
            -119.3, -119.3, -119.6, -119.9, -119.8, -119.8, -120.0, -119.9, -120.5,
        ]),
    ],
    "Mantra": [
        ("session 1", [
            -101.5, -108.8, -111.5, -112.5, -112.7, -115.8, -116.7, -117.2, -117.5,
            -117.4, -109.5, -110.4, -115.5, -117.3, -119.3, -120.4, -120.8, -121.0,
            -113.7, -121.0, -120.8, -120.6, -120.6, -120.3, -120.4, -121.2, -122.0,
            -122.3, -122.7, -122.8, -123.0, -123.1, -123.3, -123.3, -123.4, -123.6,
            -123.4, -123.6, -123.9, -123.9, -123.7, -123.8, -123.7, -124.2, -123.9,
        ]),
    ],
    "Open Awareness": [
        ("session 1", [
            -103.3, -110.8, -113.2, -114.1, -114.3, -117.4, -118.8, -119.1, -119.0,
            -118.4, -112.2, -113.5, -118.8, -120.2, -121.0, -121.9, -122.7, -123.4,
            -123.4, -114.0, -123.4, -123.2, -123.2, -123.8, -124.7, -125.3, -125.5,
            -125.9, -125.8, -126.0, -126.1, -126.2, -126.2, -126.4, -126.3, -126.5,
            -126.7, -127.2, -127.1, -126.9, -127.1, -127.0, -126.9, -127.2, -127.4,
        ]),
    ],
}


def init_library_state():
    if "library_page" not in st.session_state:
        st.session_state["library_page"] = st.query_params.get("library_page", "overview")
    if "library_selected_exercise" not in st.session_state:
        st.session_state["library_selected_exercise"] = st.query_params.get("exercise")
    if "library_flash_message" not in st.session_state:
        st.session_state["library_flash_message"] = None
    if "library_pending_delete" not in st.session_state:
        st.session_state["library_pending_delete"] = None


def render_library_card():
    render_card(
        "Library",
        "Browse meditation techniques and revisit your progress exercise by exercise.",
        ROUTE_ID,
    )


def _set_library_page(page: str, exercise: str | None = None):
    st.session_state["library_page"] = page
    st.session_state["library_selected_exercise"] = exercise
    st.query_params["view"] = ROUTE_ID
    st.query_params["library_page"] = page
    if exercise:
        st.query_params["exercise"] = exercise
    elif "exercise" in st.query_params:
        del st.query_params["exercise"]


def _matching_exercises(exercises: list[str], query: str) -> list[str]:
    if not query:
        return exercises
    query_lower = query.strip().lower()
    matches = []
    for exercise in exercises:
        metadata = get_exercise_details(exercise)
        category = metadata.get("category", "")
        if query_lower in exercise.lower() or query_lower in category.lower():
            matches.append(exercise)
    return matches


def _exercise_stats(exercise: str, data: dict) -> dict:
    sessions = [session for session in data["sessions"] if session["exercise"] == exercise]
    total_minutes = sum(session["duration_min"] for session in sessions)
    last_session = sessions[-1]["ts"] if sessions else None
    last_score = sessions[-1]["score"] if sessions else None
    return {
        "count": data["counts"].get(exercise, 0),
        "average": data["averages"].get(exercise),
        "sessions": sessions,
        "total_minutes": total_minutes,
        "last_session": last_session,
        "last_score": last_score,
    }


def _format_timestamp(iso_timestamp: str | None) -> str:
    if not iso_timestamp:
        return "Not practiced yet"
    try:
        parsed = datetime.fromisoformat(iso_timestamp)
    except ValueError:
        return iso_timestamp
    return parsed.strftime("%b %d, %Y")


def _render_exercise_card(exercise: str, data: dict, key_prefix: str):
    stats = _exercise_stats(exercise, data)
    metadata = get_exercise_details(exercise)
    with st.container():
        st.markdown('<div class="library-card-shell">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="library-card-header">
                <div class="library-card-kicker">{metadata["category"]}</div>
                {"<div class='library-card-badge'>Custom</div>" if metadata.get("is_custom") else ""}
            </div>
            <div class="library-card-title">{exercise}</div>
            <div class="library-card-copy">{metadata["summary"]}</div>
            """,
            unsafe_allow_html=True,
        )
        stat_line = (
            f"{stats['count']} session{'s' if stats['count'] != 1 else ''}"
            if stats["count"]
            else "No sessions yet"
        )
        average_line = (
            f"Average score {stats['average']:.2f}" if stats["average"] is not None else "Ready to explore"
        )
        st.caption(f"{stat_line} • {average_line}")
        if st.button("Open technique", key=f"{key_prefix}_{exercise}", use_container_width=True):
            _set_library_page("detail", exercise)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def _parse_timestamp(timestamp: str | None) -> datetime | None:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError:
        return None


def _most_recent_use_timestamp(exercise: str, data: dict) -> datetime | None:
    metadata = get_exercise_details(exercise)
    custom_created_at = _parse_timestamp(metadata.get("created_at"))
    session_times = [
        _parse_timestamp(session["ts"])
        for session in data["sessions"]
        if session["exercise"] == exercise
    ]
    valid_session_times = [session_time for session_time in session_times if session_time is not None]
    all_times = valid_session_times + ([custom_created_at] if custom_created_at is not None else [])
    if not all_times:
        return None
    return max(all_times)


def _featured_exercises(data: dict) -> list[str]:
    exercises = data["exercises"]
    ranked = []
    unranked = []

    for original_index, exercise in enumerate(exercises):
        latest_use = _most_recent_use_timestamp(exercise, data)
        if latest_use is None:
            unranked.append((original_index, exercise))
        else:
            ranked.append((latest_use, original_index, exercise))

    ranked.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    featured = [exercise for _, _, exercise in ranked[:FEATURED_EXERCISE_LIMIT]]

    if len(featured) < FEATURED_EXERCISE_LIMIT:
        remaining = [exercise for _, exercise in unranked if exercise not in featured]
        featured.extend(remaining[: FEATURED_EXERCISE_LIMIT - len(featured)])

    return featured


def _render_see_all_card(total_count: int):
    with st.container():
        st.markdown('<div class="library-card-shell library-card-shell--ghost">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="library-card-kicker">Library</div>
            <div class="library-card-title">See all</div>
            <div class="library-card-copy">
                Browse all {total_count} techniques in one searchable view.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("See all techniques", key="library_see_all", use_container_width=True):
            _set_library_page("all")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def _render_score_evolution_chart(exercise: str, sessions: list[dict]):
    if not sessions:
        st.info("Your score trend will appear here after you log sessions for this technique.")
        return

    dated_sessions = []
    for session in sessions:
        parsed = _parse_timestamp(session["ts"])
        if parsed is None:
            continue
        dated_sessions.append((parsed, session["score"]))

    if not dated_sessions:
        st.info("No timestamped sessions are available for plotting yet.")
        return

    dated_sessions.sort(key=lambda item: item[0])
    dates = [item[0] for item in dated_sessions]
    scores = [item[1] for item in dated_sessions]

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    fig.patch.set_facecolor("#fffaf3")
    ax.set_facecolor("#fffaf3")
    ax.plot(dates, scores, color="#405244", linewidth=2.2, marker="o", markersize=5)
    ax.fill_between(dates, scores, [0] * len(scores), color="#9caf88", alpha=0.15)
    ax.set_title(f"{exercise} over time", fontsize=10, color="#556054", pad=10)
    ax.set_ylim(0, 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d8d2c6")
    ax.spines["bottom"].set_color("#d8d2c6")
    ax.tick_params(axis="x", labelrotation=30, labelsize=8, colors="#7a7468")
    ax.tick_params(axis="y", labelsize=8, colors="#7a7468")
    ax.grid(axis="y", color="#d8d2c6", alpha=0.45, linewidth=0.8)
    fig.tight_layout()
    st.pyplot(fig)


def _render_power_band_evolution_chart(exercise: str):
    fig, ax = plt.subplots(figsize=(12, 4.6))
    fig.patch.set_facecolor("#fffaf3")
    ax.set_facecolor("#fffaf3")

    band_regions = [
        ("Delta", 1, 4, "#d9edf7"),
        ("Theta", 4, 8, "#d8f3dc"),
        ("Alpha", 8, 12, "#f8f1d2"),
        ("Beta", 12, 30, "#f7d9cb"),
        ("Gamma", 30, 45, "#ead9f5"),
    ]
    for label, start, end, color in band_regions:
        ax.axvspan(start, end, color=color, alpha=0.55, label=label)

    line_colors = {
        "session 1": "#ff7f0e",
        "session 2": "#1f77b4",
        "session 3": "#2ca02c",
    }
    series_to_plot = POWER_BAND_EXERCISE_SERIES.get(
        exercise,
        list(POWER_BAND_SERIES.items()),
    )
    for label, values in series_to_plot:
        ax.plot(
            POWER_BAND_FREQUENCIES,
            values,
            linewidth=1.9,
            color=line_colors[label],
            label=label,
        )

    ax.set_title(exercise, fontsize=14, color="#1f1f1f", pad=8)
    ax.set_xlabel("Frequency (Hz)", fontsize=10)
    ax.set_ylabel("Power (dB)", fontsize=10)
    ax.set_xlim(0, 47)
    ax.set_ylim(-132.5, -92.5)
    ax.spines["top"].set_color("#222222")
    ax.spines["right"].set_color("#222222")
    ax.spines["left"].set_color("#222222")
    ax.spines["bottom"].set_color("#222222")
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#c7c7c7")
    fig.tight_layout()
    st.pyplot(fig)


def _exercise_logbook_entries(exercise: str, sessions: list[dict]) -> list[dict]:
    entries = []
    for index, session in enumerate(sessions):
        if session.get("journal_grade") is None and not session.get("journal_note"):
            continue
        parsed = _parse_timestamp(session.get("ts"))
        entries.append(
            {
                **session,
                "_entry_id": f"{exercise}_logbook_{index}",
                "_parsed_time": parsed or datetime.min,
            }
        )

    entries.sort(key=lambda item: item["_parsed_time"], reverse=True)
    return entries


def _render_exercise_logbook(exercise: str, sessions: list[dict]):
    entries = _exercise_logbook_entries(exercise, sessions)
    if not entries:
        st.info("The notes linked to this exercise will appear here after you save a Logbook entry.")
        return

    state_key = f"selected_logbook_entry_{exercise}"
    valid_ids = {entry["_entry_id"] for entry in entries}
    if st.session_state.get(state_key) not in valid_ids:
        st.session_state[state_key] = entries[0]["_entry_id"]

    list_col, detail_col = st.columns([1.2, 1.8], gap="large")

    with list_col:
        for entry in entries:
            label = _format_timestamp(entry.get("ts"))
            button_type = (
                "primary"
                if st.session_state.get(state_key) == entry["_entry_id"]
                else "secondary"
            )
            if st.button(
                label,
                key=entry["_entry_id"],
                use_container_width=True,
                type=button_type,
            ):
                st.session_state[state_key] = entry["_entry_id"]
                st.rerun()

    selected_entry = next(
        entry for entry in entries if entry["_entry_id"] == st.session_state[state_key]
    )

    with detail_col:
        metric_left, metric_right = st.columns(2)
        with metric_left:
            journal_grade = selected_entry.get("journal_grade")
            st.metric(
                "Self-grade",
                f"{journal_grade}/10" if journal_grade is not None else "N/A",
            )
        with metric_right:
            score = selected_entry.get("score")
            st.metric(
                "Computed score",
                f"{score:.2f}" if score is not None else "N/A",
            )

        st.caption(
            f"{_format_timestamp(selected_entry.get('ts'))} • {selected_entry.get('duration_min', 'N/A')} min"
        )
        st.markdown("**Your note**")
        note = selected_entry.get("journal_note", "").strip()
        if note:
            st.write(note)
        else:
            st.write("_No note written for this session._")


def _render_compact_stat(label: str, value: str):
    st.markdown(
        f"""
        <div class="library-stat-card">
            <div class="library-stat-label">{label}</div>
            <div class="library-stat-value library-stat-value--small">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_cards_grid(exercises: list[str], data: dict, key_prefix: str, include_see_all: bool = False):
    card_items = list(exercises)
    if include_see_all:
        card_items.append("__see_all__")

    for row_start in range(0, len(card_items), 3):
        row_items = card_items[row_start:row_start + 3]
        columns = st.columns(3, gap="large")
        for column, item in zip(columns, row_items):
            with column:
                if item == "__see_all__":
                    _render_see_all_card(len(data["exercises"]))
                else:
                    _render_exercise_card(item, data, key_prefix)
        for column in columns[len(row_items):]:
            with column:
                st.empty()


def _render_library_header(on_back, title: str, caption: str):
    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.title(title)
        st.caption(caption)
    with top_right:
        if on_back is not None and st.button("Back", use_container_width=True):
            on_back()
            st.rerun()
    flash_message = st.session_state.get("library_flash_message")
    if flash_message:
        st.success(flash_message)
        st.session_state["library_flash_message"] = None


def _delete_custom_exercise(exercise: str):
    delete_exercise(exercise)
    st.session_state["library_flash_message"] = f'"{exercise}" was deleted from the library.'
    st.session_state["library_pending_delete"] = None
    _set_library_page("overview")
    st.rerun()


def _open_delete_confirmation(exercise: str):
    if hasattr(st, "dialog"):
        @st.dialog("Delete custom exercise")
        def confirm_delete_dialog():
            st.write(
                "This will permanently remove the custom exercise and all of its session history."
            )
            confirm_col, cancel_col = st.columns(2)
            with confirm_col:
                if st.button("Delete permanently", type="primary", use_container_width=True):
                    _delete_custom_exercise(exercise)
            with cancel_col:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        confirm_delete_dialog()
        return

    st.session_state["library_pending_delete"] = exercise


def _render_custom_exercise_form():
    st.divider()
    st.subheader("Submit your own exercise")
    st.caption("Add a custom meditation technique to the library and make it available in the session planner.")
    available_categories = get_exercise_categories()

    with st.form("library_custom_exercise_form", clear_on_submit=True):
        name = st.text_input("Exercise name")
        category = st.selectbox("Category", available_categories)
        description = st.text_area("Description")
        tutorial = st.text_area(
            "Tutorial",
            placeholder="Write one step per line on how to perform this meditation exercise.",
        )
        guide_data = st.text_area(
            "Guide data - yet to determine data format and content",
            placeholder="Use free text for now, such as prompts, pacing notes, or guidance logic.",
        )
        precision_criteria = st.text_area(
            "Precision criteria data - yet to determine data format and content",
            placeholder="Use free text for now, such as posture checks, breathing targets, or evaluation notes.",
        )
        submitted = st.form_submit_button("Add custom exercise", use_container_width=True)

    if not submitted:
        return

    clean_name = name.strip()
    if not clean_name:
        st.error("Add an exercise name before saving.")
        return
    if clean_name in load_data()["exercises"]:
        st.error("That exercise name already exists in the library. Choose a different name.")
        return

    tutorial_steps = [step.strip() for step in tutorial.splitlines() if step.strip()]
    add_exercise(
        clean_name,
        category=category,
        description=description,
        how_to=tutorial_steps,
        guide_data=guide_data,
        precision_criteria=precision_criteria,
    )
    st.success(f'"{clean_name}" was added to the library and can now be selected in the session planner.')
    st.rerun()


def _render_overview(on_back, data: dict):
    _render_library_header(
        on_back,
        "Library",
        "Explore saved meditation techniques and open a dedicated page for each one.",
    )
    query = st.text_input(
        "Search techniques",
        key="library_search_overview",
        placeholder="Look up a meditation exercise",
    )
    exercises = data["exercises"]
    filtered = _matching_exercises(exercises, query)
    if query.strip():
        st.caption(f"{len(filtered)} matching technique{'s' if len(filtered) != 1 else ''}")
        if not filtered:
            st.info("No techniques matched that search.")
            _render_custom_exercise_form()
            return
        _render_cards_grid(filtered, data, "library_search", include_see_all=False)
        _render_custom_exercise_form()
        return

    visible = _featured_exercises(data)
    _render_cards_grid(visible, data, "library_overview", include_see_all=True)
    _render_custom_exercise_form()


def _render_all_exercises(on_back, data: dict):
    _render_library_header(
        on_back,
        "All techniques",
        "Every meditation technique currently available in the library.",
    )
    if st.button("Back to featured", key="library_back_overview"):
        _set_library_page("overview")
        st.rerun()
    query = st.text_input(
        "Search all techniques",
        key="library_search_all",
        placeholder="Filter the full library",
    )
    filtered = _matching_exercises(data["exercises"], query)
    if not filtered:
        st.info("No techniques matched that search.")
        _render_custom_exercise_form()
        return
    st.caption(f"{len(filtered)} technique{'s' if len(filtered) != 1 else ''} shown")
    _render_cards_grid(filtered, data, "library_all", include_see_all=False)
    _render_custom_exercise_form()


def _render_detail(on_back, data: dict):
    exercise = st.session_state.get("library_selected_exercise")
    if not exercise or exercise not in data["exercises"]:
        _set_library_page("overview")
        st.rerun()
        return

    metadata = get_exercise_details(exercise)
    stats = _exercise_stats(exercise, data)

    _render_library_header(
        on_back,
        exercise,
        f'{metadata["category"]} • Individual technique page with guidance and user stats.',
    )
    back_left, back_right, delete_col = st.columns([1.3, 1.4, 1.7])
    with back_left:
        if st.button("Back to library", key="library_detail_back"):
            _set_library_page("overview")
            st.rerun()
    with back_right:
        if st.button("See all techniques", key="library_detail_all"):
            _set_library_page("all")
            st.rerun()
    with delete_col:
        if metadata.get("is_custom") and st.button(
            "Delete custom exercise",
            key="library_detail_delete",
            use_container_width=True,
        ):
            _open_delete_confirmation(exercise)

    with st.container():
        st.markdown('<div class="library-detail-panel">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="library-card-header">
                <div class="library-card-kicker">{metadata["category"]}</div>
                {"<div class='library-card-badge'>Custom</div>" if metadata.get("is_custom") else ""}
            </div>
            <div class="library-card-title">{exercise}</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="library-section-intro">', unsafe_allow_html=True)
    st.markdown(f"**Type of meditation:** {metadata['category']}")
    st.write(metadata["description"])
    st.markdown("</div>", unsafe_allow_html=True)

    if metadata.get("is_custom") and st.session_state.get("library_pending_delete") == exercise:
        st.warning(
            "Deleting this custom exercise will also remove all of its logged history."
        )
        confirm_col, cancel_col = st.columns(2)
        with confirm_col:
            if st.button("Confirm delete", key="library_inline_confirm_delete", type="primary"):
                _delete_custom_exercise(exercise)
        with cancel_col:
            if st.button("Cancel", key="library_inline_cancel_delete"):
                st.session_state["library_pending_delete"] = None
                st.rerun()

    metric_one, metric_two, metric_three, metric_four = st.columns(4)
    with metric_one:
        st.metric("Sessions", stats["count"])
    with metric_two:
        st.metric("Average score", f"{stats['average']:.2f}" if stats["average"] is not None else "N/A")
    with metric_three:
        st.metric("Minutes practiced", stats["total_minutes"])
    with metric_four:
        _render_compact_stat("Last session", _format_timestamp(stats["last_session"]))

    st.divider()
    guidance_col, snapshot_col = st.columns([3, 2], gap="large")
    with guidance_col:
        st.subheader("How to practice")
        for step_number, step in enumerate(metadata["how_to"], start=1):
            st.markdown(f"{step_number}. {step}")
        if metadata.get("guide_data"):
            st.subheader("Guide data")
            st.write(metadata["guide_data"])
        if metadata.get("precision_criteria"):
            st.subheader("Precision criteria")
            st.write(metadata["precision_criteria"])
    with snapshot_col:
        st.subheader("Snapshot")
        if stats["count"] == 0:
            st.info("This technique has not been logged yet.")
        else:
            st.write(
                f"You have practiced **{exercise}** {stats['count']} time"
                f"{'s' if stats['count'] != 1 else ''}."
            )
            if stats["last_score"] is not None:
                st.write(f"Most recent session score: **{stats['last_score']:.2f}**")

    st.divider()
    st.subheader("Score evolution")
    _render_score_evolution_chart(exercise, stats["sessions"])

    st.subheader("Power band evolution")
    _render_power_band_evolution_chart(exercise)

    st.divider()
    st.subheader("Logbook")
    _render_exercise_logbook(exercise, stats["sessions"])

    st.divider()
    st.subheader("Recent sessions")
    if not stats["sessions"]:
        st.info("Once this technique is logged, its recent sessions will appear here.")
        return

    for session in reversed(stats["sessions"][-5:]):
        session_date = _format_timestamp(session["ts"])
        st.markdown(
            f"**{session_date}**  •  Score `{session['score']:.2f}`  •  {session['duration_min']} min"
        )


def render_library_view(on_back=None):
    init_library_state()
    data = load_data()
    page = st.session_state.get("library_page", "overview")
    if page == "detail":
        _render_detail(on_back, data)
    elif page == "all":
        _render_all_exercises(on_back, data)
    else:
        _render_overview(on_back, data)
