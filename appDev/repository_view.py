from datetime import datetime
from html import escape
from textwrap import dedent

import streamlit as st

from utils import get_exercise_details, load_data


def init_repository_state():
    """Repository is a single feed page in V1."""
    return


MEDITATION_MODELS = [
    {
        "title": "Vipasanna model",
        "category": "Attention model",
        "summary": "A focused observation model for tracking clarity, sustained attention, and stable breath-led awareness.",
        "parameters": [
            "EEG alpha power",
            "EEG beta activity",
            "EEG gamma bursts",
            "Breath rhythm stability",
            "ECG heart rate",
        ],
    },
    {
        "title": "Non dual awareness model",
        "category": "Awareness model",
        "summary": "A spacious awareness model for observing open-monitoring states, low reactivity, and non-contracted attention.",
        "parameters": [
            "EEG gamma synchrony",
            "EEG alpha coherence",
            "EEG frontal asymmetry",
            "ECG HRV balance",
            "Stillness index",
        ],
    },
    {
        "title": "Non sleep deep rest",
        "category": "Recovery model",
        "summary": "A restorative model focused on down-regulation, deep rest, and nervous-system recovery without sleep onset.",
        "parameters": [
            "EEG theta drift",
            "EEG alpha-theta ratio",
            "ECG resting pulse",
            "ECG recovery trend",
            "Body relaxation marker",
        ],
    },
]


def _parse_timestamp(timestamp: str | None) -> datetime | None:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError:
        return None


def _format_timestamp(timestamp: str | None) -> str:
    parsed = _parse_timestamp(timestamp)
    if parsed is None:
        return timestamp or "No recent activity"
    return parsed.strftime("%b %d, %H:%M")


def _popular_practices(data: dict) -> list[str]:
    exercises = list(data["exercises"])
    exercises.sort(
        key=lambda exercise: (
            data["counts"].get(exercise, 0),
            data["averages"].get(exercise, 0.0),
        ),
        reverse=True,
    )
    return exercises[:6]


def _community_highlights(data: dict) -> list[dict]:
    exercises = _popular_practices(data)[:3]
    highlights = []
    community_names = ["Mila", "Jonas", "Ari"]
    for idx, exercise in enumerate(exercises):
        metadata = get_exercise_details(exercise)
        count = data["counts"].get(exercise, 0)
        highlights.append(
            {
                "name": community_names[idx % len(community_names)],
                "exercise": exercise,
                "category": metadata.get("category", "Technique"),
                "summary": metadata.get("summary", "Shared with the community."),
                "count": count,
            }
        )
    return highlights


def _render_repository_header(on_back):
    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.title("Global repository")
        st.caption("A public feed for shared meditation practices and the future of open contemplative data.")
    with top_right:
        if on_back is not None and st.button("Back", use_container_width=True, key="repository_back_home"):
            on_back()
            st.rerun()


def _render_hero():
    st.markdown(
        """
        <div class="repository-hero">
            <div class="repository-hero-kicker">Open meditation commons</div>
            <div class="repository-hero-title">See what the community is sharing, practicing, and building toward.</div>
            <div class="repository-hero-copy">
                Global repository is where meditation techniques become public, remixable, and eventually linkable to
                richer physiological research like EEG, ECG, and HRV.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_meditation_models():
    st.markdown(
        dedent(
            """
            <div class="repository-section-head">
                <div class="repository-section-title">Meditation models</div>
                <div class="repository-section-copy">Model templates for the rich physiological parameters this repository can eventually organize.</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    columns = st.columns(3, gap="large")
    for column, model in zip(columns, MEDITATION_MODELS):
        with column:
            parameter_tags = "".join(
                f"<span>{escape(parameter)}</span>" for parameter in model["parameters"]
            )
            st.markdown(
                dedent(
                    f"""
                    <div class="repository-feed-card">
                        <div class="repository-card-topline">
                            <div class="repository-card-kicker">{escape(model["category"])}</div>
                            <div class="repository-card-badge">Model</div>
                        </div>
                        <div class="repository-card-title">{escape(model["title"])}</div>
                        <div class="repository-card-copy">{escape(model["summary"])}</div>
                        <div class="repository-model-params">
                            {parameter_tags}
                        </div>
                    </div>
                    """
                ).strip(),
                unsafe_allow_html=True,
            )


def _render_community_highlights(data: dict):
    st.markdown(
        dedent(
            """
            <div class="repository-section-head">
                <div class="repository-section-title">Community highlights</div>
                <div class="repository-section-copy">Early signals of the social layer this repository can grow into.</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    highlights = _community_highlights(data)
    if not highlights:
        st.info("Highlights will appear as the repository grows.")
        return

    columns = st.columns(3, gap="large")
    for column, item in zip(columns, highlights):
        with column:
            st.markdown(
                dedent(
                    f"""
                    <div class="repository-highlight-card">
                        <div class="repository-highlight-name">{escape(str(item['name']))}</div>
                        <div class="repository-highlight-title">{escape(str(item['exercise']))}</div>
                        <div class="repository-highlight-copy">{escape(str(item['summary']))}</div>
                        <div class="repository-highlight-meta">{escape(str(item['category']))} - {item['count']} community sessions</div>
                    </div>
                    """
                ).strip(),
                unsafe_allow_html=True,
            )


def _render_future_teaser():
    st.markdown(
        """
        <div class="repository-teaser-shell">
            <div class="repository-teaser-title">Future open-data layer</div>
            <div class="repository-teaser-copy">
                This feed is the public front door. Next, it can expand into a shared research layer with
                EEG, ECG, and HRV uploads, anonymized session bundles, community comparisons, and friend activity.
            </div>
            <div class="repository-teaser-pills">
                <span>EEG uploads</span>
                <span>ECG + HRV</span>
                <span>Friend activity</span>
                <span>Open contemplative research</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    teaser_left, teaser_right = st.columns([1.05, 1.6], gap="large")
    with teaser_left:
        st.button("Upload to repository", use_container_width=True, disabled=True)
    with teaser_right:
        st.markdown(
            """
            <div class="repository-inline-note">
                Uploads stay intentionally disabled in V1 so the repository can communicate direction without pretending the
                full data workflow already exists.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_repository_view(on_back=None):
    data = load_data()

    _render_repository_header(on_back)
    _render_hero()
    _render_meditation_models()
    st.divider()
    _render_community_highlights(data)
    st.divider()
    _render_future_teaser()
