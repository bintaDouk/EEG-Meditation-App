import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from session_planner import init_planner_state, render_session_planner


def init_app_state():
    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"


def go_to(view_name: str):
    st.session_state.current_view = view_name


def render_app_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f7f4ee 0%, #f1ede5 100%);
            color: #1f2a21;
        }
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #f7f4ee 0%, #f1ede5 100%);
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1rem;
            padding-bottom: 2.5rem;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        [data-testid="stToolbar"] {
            right: 1rem;
        }
        .stMarkdown, .stCaption, label, p, h1, h2, h3 {
            color: #1f2a21;
        }
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="popover"] {
            background-color: #ffffff;
            border-color: rgba(124, 116, 103, 0.18);
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] div {
            color: #1f2a21;
        }
        div[data-baseweb="select"] svg {
            fill: #1f2a21;
            color: #1f2a21;
            stroke: #1f2a21;
            opacity: 1;
        }
        .stRadio > div,
        .stToggle label,
        .stSelectbox label,
        .stTextArea label,
        .stSlider label {
            color: #2f382f;
        }
        .stButton > button {
            background: #d6e0d1;
            color: #1f2a21 !important;
            border: 1px solid rgba(71, 89, 72, 0.18);
            border-radius: 999px;
            min-height: 2.8rem;
            font-weight: 600;
        }
        .stButton > button * {
            color: inherit !important;
        }
        .stButton > button:hover {
            border-color: rgba(71, 89, 72, 0.28);
            color: #1f2a21 !important;
        }
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {
            background: #1f2a21;
            color: #f7f4ee !important;
            border-color: #1f2a21;
        }
        .stButton > button[kind="primary"] *,
        .stButton > button[data-testid="baseButton-primary"] * {
            color: #f7f4ee !important;
            fill: #f7f4ee !important;
        }
        div[data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 22px;
        }
        [data-testid="stMetric"] {
            background: rgba(255, 252, 247, 0.72);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 18px;
            padding: 0.8rem;
        }
        .planner-shell {
            background: rgba(255, 252, 247, 0.72);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 24px;
            padding: 1.4rem;
            box-shadow: 0 18px 40px rgba(78, 72, 61, 0.06);
        }
        .quote-card {
            background: rgba(214, 224, 209, 0.32);
            border: 1px solid rgba(71, 89, 72, 0.14);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-top: 0.75rem;
            margin-bottom: 1.35rem;
            color: #334033;
            text-align: left;
        }
        .quote-author {
            display: block;
            margin-top: 0.85rem;
            text-align: left;
            font-weight: 600;
        }
        .hero {
            text-align: center;
            padding: 2rem 0 2rem;
        }
        .hero-kicker {
            font-size: 3.2rem;
            line-height: 1.05;
            color: #1f2a21;
            margin-bottom: 0.9rem;
            font-weight: 600;
        }
        .hero-title {
            letter-spacing: 0.16em;
            text-transform: uppercase;
            font-size: 0.78rem;
            color: #7a7468;
            margin-bottom: 0.8rem;
        }
        .hero-copy {
            max-width: 38rem;
            margin: 0 auto;
            color: #5f655e;
            font-size: 1.05rem;
            line-height: 1.8;
        }
        .card {
            background: rgba(255, 252, 247, 0.88);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 1.4rem 1.2rem;
            min-height: 190px;
            box-shadow: 0 18px 40px rgba(78, 72, 61, 0.06);
        }
        .card-title {
            color: #1f2a21;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .card-copy {
            color: #61675f;
            line-height: 1.65;
            margin-bottom: 1.2rem;
        }
        .placeholder {
            color: #877f72;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Open Source Meditation</div>
            <div class="hero-title">A quieter way to begin</div>
            <div class="hero-copy">
                Choose how you want to practice, begin a new session, or return to your
                meditation history when those views are ready.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    start_col, submit_col, analytics_col = st.columns(3, gap="large")

    with start_col:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Begin meditation</div>
                <div class="card-copy">
                    Start a new practice with a calm session planner and device preview.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open planner", use_container_width=True, key="home_begin"):
            go_to("planner")
            st.rerun()

    with submit_col:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Submit recorded session</div>
                <div class="card-copy">
                    Upload a completed session from another workflow.
                </div>
                <div class="placeholder">Empty for the pitch.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open submit", use_container_width=True, key="home_submit"):
            go_to("submit")
            st.rerun()

    with analytics_col:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Previous session analytics</div>
                <div class="card-copy">
                    Review your earlier practice sessions and results.
                </div>
                <div class="placeholder">Empty for the pitch.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open analytics", use_container_width=True, key="home_analytics"):
            go_to("analytics")
            st.rerun()


def render_placeholder_view(title: str, message: str):
    if st.button("Back", key=f"back_{title.lower().replace(' ', '_')}"):
        go_to("home")
        st.rerun()

    st.title(title)
    st.caption(message)
    st.info("This section is intentionally left empty for the pitch demo.")


def render_results_view():
    categories = ["Speed", "Power", "Skill", "Agility", "Stamina"]
    values = [3, 4, 5, 2, 4]

    count = len(categories)
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False).tolist()

    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    st.pyplot(fig)


def main():
    st.set_page_config(
        page_title="Open Source Meditation",
        page_icon="OM",
        layout="centered",
    )

    render_app_styles()
    init_app_state()
    init_planner_state()

    current_view = st.session_state.current_view

    if current_view == "home":
        render_home()
    elif current_view == "planner":
        render_session_planner(on_back=lambda: go_to("home"))
    elif current_view == "submit":
        render_placeholder_view(
            "Submit recorded session",
            "Use this space later for manual uploads or imported recordings.",
        )
    elif current_view == "analytics":
        render_placeholder_view(
            "Previous session analytics",
            "This route is reserved for the teammate-owned analytics experience.",
        )
    elif current_view == "results":
        render_results_view()
    else:
        go_to("home")
        st.rerun()


if __name__ == "__main__":
    main()
