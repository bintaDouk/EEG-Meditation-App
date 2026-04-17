import streamlit as st


def render_app_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #ffffff;
            color: #1f2a21;
        }
        [data-testid="stAppViewContainer"] {
            background: #ffffff;
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
        [data-testid="stMetric"] {
            background: rgba(255, 252, 247, 0.72);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 18px;
            padding: 0.8rem;
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
        a.home-card,
        a.home-card:visited,
        a.home-card:hover,
        a.home-card:active {
            display: block;
            min-height: 190px;
            padding: 1.4rem 1.2rem;
            background: #e3ebdf;
            border: 1px solid rgba(71, 89, 72, 0.18);
            border-radius: 22px;
            box-shadow: 0 18px 40px rgba(78, 72, 61, 0.05);
            color: #1f2a21 !important;
            text-decoration: none !important;
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
        }
        a.home-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 22px 48px rgba(78, 72, 61, 0.1);
            border-color: rgba(71, 89, 72, 0.3);
        }
        .home-card-title {
            display: block;
            color: #1f2a21;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
            line-height: 1.35;
        }
        .home-card-copy {
            display: block;
            color: #61675f;
            font-size: 1rem;
            line-height: 1.65;
        }
        .session-run-timer {
            font-size: 4.4rem;
            line-height: 1;
            font-weight: 600;
            color: #1f2a21;
            margin: 0.6rem 0 1rem;
        }
        .intro-player-shell {
            background: rgba(255, 252, 247, 0.88);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        .intro-player-screen {
            min-height: 230px;
            padding: 1.25rem;
            background: linear-gradient(180deg, #273229 0%, #1f2a21 100%);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        .intro-player-badge {
            color: rgba(247, 244, 238, 0.76);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-size: 0.76rem;
            margin-bottom: 0.5rem;
        }
        .intro-player-time {
            color: #f7f4ee;
            font-size: 3.6rem;
            line-height: 1;
            font-weight: 600;
            margin-bottom: 0.6rem;
        }
        .intro-player-subtitle {
            color: rgba(247, 244, 238, 0.8);
            font-size: 1rem;
            line-height: 1.6;
            max-width: 26rem;
        }
        .intro-player-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
            padding: 0.9rem 1rem;
            background: rgba(255, 252, 247, 0.94);
        }
        .intro-player-dot {
            width: 0.75rem;
            height: 0.75rem;
            border-radius: 999px;
            background: #d05f43;
            flex-shrink: 0;
        }
        .intro-player-meta {
            color: #5f655e;
            font-size: 0.92rem;
        }
        .guided-media-shell {
            background: rgba(255, 252, 247, 0.86);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.8rem;
        }
        .guided-media-title {
            font-size: 1rem;
            font-weight: 600;
            color: #1f2a21;
            margin-bottom: 0.35rem;
        }
        .guided-media-copy {
            color: #61675f;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
