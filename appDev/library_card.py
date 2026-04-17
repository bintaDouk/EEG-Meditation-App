from datetime import datetime

import matplotlib.pyplot as plt
import streamlit as st

from home_cards import render_card
from utils import add_exercise, get_exercise_details, load_data


ROUTE_ID = "library"
FEATURED_EXERCISE_LIMIT = 5


def init_library_state():
    if "library_page" not in st.session_state:
        st.session_state["library_page"] = st.query_params.get("library_page", "overview")
    if "library_selected_exercise" not in st.session_state:
        st.session_state["library_selected_exercise"] = st.query_params.get("exercise")


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
    return [exercise for exercise in exercises if query_lower in exercise.lower()]


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
    st.subheader("Score evolution")
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

    fig, ax = plt.subplots(figsize=(4.6, 2.8))
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


def _render_custom_exercise_form():
    st.divider()
    st.subheader("Submit your own exercise")
    st.caption("Add a custom meditation technique to the library and make it available in the session planner.")

    with st.form("library_custom_exercise_form", clear_on_submit=True):
        name = st.text_input("Exercise name")
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
    back_left, back_right, _ = st.columns([1.3, 1.4, 3])
    with back_left:
        if st.button("Back to library", key="library_detail_back"):
            _set_library_page("overview")
            st.rerun()
    with back_right:
        if st.button("See all techniques", key="library_detail_all"):
            _set_library_page("all")
            st.rerun()

    with st.container():
        st.markdown('<div class="library-detail-panel">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="library-card-header">
                <div class="library-card-kicker">{metadata["category"]}</div>
                {"<div class='library-card-badge'>Custom</div>" if metadata.get("is_custom") else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(metadata["description"])
        st.markdown("</div>", unsafe_allow_html=True)

    metric_one, metric_two, metric_three, metric_four = st.columns(4)
    with metric_one:
        st.metric("Sessions", stats["count"])
    with metric_two:
        st.metric("Average score", f"{stats['average']:.2f}" if stats["average"] is not None else "N/A")
    with metric_three:
        st.metric("Minutes practiced", stats["total_minutes"])
    with metric_four:
        st.metric("Last session", _format_timestamp(stats["last_session"]))

    guidance_col, stats_col = st.columns([3, 2], gap="large")
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
    with stats_col:
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
        _render_score_evolution_chart(exercise, stats["sessions"])

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
