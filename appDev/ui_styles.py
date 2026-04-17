import streamlit as st
import streamlit.components.v1 as components


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
            min-height: 214px;
            padding: 1.55rem 1.35rem;
            background: #f3eee3;
            border: 1px solid rgba(124, 116, 103, 0.16);
            border-radius: 24px;
            box-shadow: 0 18px 40px rgba(78, 72, 61, 0.06);
            color: #1f2a21 !important;
            text-decoration: none !important;
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
        }
        a.home-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 22px 48px rgba(78, 72, 61, 0.1);
            border-color: rgba(111, 138, 111, 0.3);
        }
        .home-card-title {
            display: block;
            color: #1f2a21;
            font-size: 1.34rem;
            font-weight: 600;
            margin-bottom: 0.78rem;
            line-height: 1.28;
        }
        .home-card-copy {
            display: block;
            color: #61675f;
            font-size: 1.02rem;
            line-height: 1.72;
        }
        .analytics-intro {
            margin-top: 1.25rem;
            margin-bottom: 1rem;
        }
        .analytics-title {
            color: #1f2a21;
            font-size: 2.35rem;
            line-height: 1.08;
            font-weight: 600;
            margin-bottom: 0;
        }
        .analytics-panel-head {
            margin-bottom: 0.45rem;
        }
        .analytics-panel-title {
            color: #1f2a21;
            font-size: 1.02rem;
            font-weight: 600;
            margin-bottom: 0;
        }
        .library-card-shell {
            min-height: 250px;
            padding: 1.2rem 1.1rem 0.35rem;
            background: linear-gradient(180deg, #f5f1e9 0%, #edf3e8 100%);
            border: 1px solid rgba(71, 89, 72, 0.16);
            border-radius: 22px;
            box-shadow: 0 18px 36px rgba(78, 72, 61, 0.05);
            margin-bottom: 1rem;
        }
        .library-card-shell--ghost {
            background: linear-gradient(180deg, #f7f4ee 0%, #ffffff 100%);
            border-style: dashed;
        }
        .library-card-kicker {
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #7a7468;
            margin-bottom: 0.55rem;
        }
        .library-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.45rem;
        }
        .library-card-header .library-card-kicker {
            margin-bottom: 0;
        }
        .library-card-badge {
            background: rgba(31, 42, 33, 0.08);
            color: #1f2a21;
            border: 1px solid rgba(31, 42, 33, 0.12);
            border-radius: 999px;
            padding: 0.2rem 0.55rem;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            white-space: nowrap;
        }
        .library-card-title {
            color: #1f2a21;
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.35;
            margin-bottom: 0.65rem;
        }
        .library-card-copy,
        .library-detail-copy {
            color: #556054;
            font-size: 0.98rem;
            line-height: 1.65;
        }
        .library-detail-panel {
            background: linear-gradient(135deg, rgba(227, 235, 223, 0.9), rgba(247, 244, 238, 0.98));
            border: 1px solid rgba(71, 89, 72, 0.14);
            border-radius: 22px;
            padding: 1.15rem 1.2rem;
            margin: 0.35rem 0 1rem;
        }
        .library-section-intro {
            margin-bottom: 0.8rem;
        }
        .library-stat-card {
            background: rgba(255, 252, 247, 0.72);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 18px;
            padding: 0.8rem;
            min-height: 104px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .library-stat-label {
            color: #7a7468;
            font-size: 0.88rem;
            margin-bottom: 0.3rem;
        }
        .library-stat-value {
            color: #1f2a21;
            font-weight: 600;
            line-height: 1.25;
        }
        .library-stat-value--small {
            font-size: 1rem;
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
        .analytics-history-card {
            background: rgba(255, 252, 247, 0.86);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 1.1rem 1.05rem 1rem;
            min-height: 515px;
            box-shadow: 0 16px 34px rgba(78, 72, 61, 0.05);
        }
        .analytics-history-title {
            color: #1f2a21;
            font-size: 1.04rem;
            font-weight: 600;
            margin-bottom: 0.95rem;
        }
        .analytics-history-scroll {
            max-height: 445px;
            overflow-y: auto;
            padding-right: 0.28rem;
        }
        .analytics-history-scroll::-webkit-scrollbar {
            width: 8px;
        }
        .analytics-history-scroll::-webkit-scrollbar-thumb {
            background: rgba(124, 116, 103, 0.28);
            border-radius: 999px;
        }
        .analytics-history-row {
            padding: 0.86rem 0;
            border-top: 1px solid rgba(124, 116, 103, 0.12);
        }
        .analytics-history-row:first-child {
            border-top: 0;
            padding-top: 0.15rem;
        }
        .analytics-history-row-top {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.28rem;
        }
        .analytics-history-exercise {
            color: #1f2a21;
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.4;
        }
        .analytics-history-duration {
            color: #51614f;
            font-size: 0.8rem;
            white-space: nowrap;
            background: rgba(111, 138, 111, 0.12);
            border: 1px solid rgba(111, 138, 111, 0.16);
            border-radius: 999px;
            padding: 0.18rem 0.52rem;
        }
        .analytics-history-time {
            color: #7a7468;
            font-size: 0.82rem;
            line-height: 1.5;
        }
        .analytics-history-empty {
            color: #61675f;
            line-height: 1.7;
            padding-top: 0.25rem;
        }
        .repository-hero {
            background: linear-gradient(135deg, rgba(243, 238, 227, 0.95), rgba(255, 252, 247, 0.98));
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 24px;
            padding: 1.35rem 1.4rem;
            margin-bottom: 1.15rem;
            box-shadow: 0 16px 34px rgba(78, 72, 61, 0.05);
        }
        .repository-hero-kicker {
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #7a7468;
            margin-bottom: 0.55rem;
        }
        .repository-hero-title {
            color: #1f2a21;
            font-size: 1.95rem;
            line-height: 1.16;
            font-weight: 600;
            margin-bottom: 0.75rem;
            max-width: 34rem;
        }
        .repository-hero-copy {
            color: #61675f;
            font-size: 1rem;
            line-height: 1.75;
            max-width: 40rem;
        }
        .repository-card-shell {
            min-height: 220px;
            background: rgba(255, 252, 247, 0.92);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 1.1rem 1.1rem 0.95rem;
            box-shadow: 0 14px 30px rgba(78, 72, 61, 0.04);
            margin-bottom: 0.85rem;
        }
        .repository-card-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.55rem;
        }
        .repository-card-kicker {
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-size: 0.7rem;
            color: #7a7468;
        }
        .repository-card-badge {
            background: rgba(111, 138, 111, 0.12);
            color: #4e624e;
            border: 1px solid rgba(111, 138, 111, 0.18);
            border-radius: 999px;
            padding: 0.22rem 0.56rem;
            font-size: 0.72rem;
            font-weight: 600;
            white-space: nowrap;
        }
        .repository-card-title {
            color: #1f2a21;
            font-size: 1.2rem;
            line-height: 1.3;
            font-weight: 600;
            margin-bottom: 0.55rem;
        }
        .repository-card-copy,
        .repository-detail-copy {
            color: #5a6358;
            font-size: 0.97rem;
            line-height: 1.68;
        }
        .repository-card-meta {
            margin-top: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.65rem;
            flex-wrap: wrap;
            color: #6f756d;
            font-size: 0.82rem;
        }
        .repository-card-meta span {
            background: rgba(243, 238, 227, 0.8);
            border: 1px solid rgba(124, 116, 103, 0.12);
            border-radius: 999px;
            padding: 0.18rem 0.5rem;
        }
        .repository-model-params {
            margin-top: 0.95rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }
        .repository-model-params span {
            background: rgba(111, 138, 111, 0.1);
            color: #4e624e;
            border: 1px solid rgba(111, 138, 111, 0.14);
            border-radius: 999px;
            padding: 0.22rem 0.55rem;
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .repository-inline-note {
            color: #6a6f67;
            font-size: 0.95rem;
            line-height: 1.65;
            padding-top: 0.2rem;
        }
        .repository-section-head {
            margin-bottom: 0.8rem;
        }
        .repository-section-title {
            color: #1f2a21;
            font-size: 1.12rem;
            font-weight: 600;
            margin-bottom: 0.22rem;
        }
        .repository-section-copy {
            color: #72776f;
            font-size: 0.92rem;
            line-height: 1.6;
        }
        .repository-feed-shell {
            background: rgba(255, 252, 247, 0.92);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 0.35rem 1.05rem;
            box-shadow: 0 14px 30px rgba(78, 72, 61, 0.04);
        }
        .repository-activity-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.9rem 0;
            border-top: 1px solid rgba(124, 116, 103, 0.12);
        }
        .repository-activity-row:first-child {
            border-top: 0;
        }
        .repository-activity-main {
            min-width: 0;
        }
        .repository-activity-exercise {
            color: #1f2a21;
            font-size: 1rem;
            line-height: 1.4;
            font-weight: 600;
            margin-bottom: 0.18rem;
        }
        .repository-activity-meta {
            color: #72776f;
            font-size: 0.84rem;
            line-height: 1.55;
        }
        .repository-activity-badge {
            background: rgba(111, 138, 111, 0.12);
            color: #4e624e;
            border: 1px solid rgba(111, 138, 111, 0.16);
            border-radius: 999px;
            padding: 0.24rem 0.58rem;
            font-size: 0.76rem;
            font-weight: 600;
            white-space: nowrap;
            flex-shrink: 0;
        }
        .repository-feed-card,
        .repository-highlight-card {
            min-height: 205px;
            background: rgba(255, 252, 247, 0.92);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 1.05rem 1.05rem 0.95rem;
            box-shadow: 0 14px 30px rgba(78, 72, 61, 0.04);
            margin-bottom: 0.85rem;
        }
        .repository-highlight-name {
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #7a7468;
            margin-bottom: 0.55rem;
        }
        .repository-highlight-title {
            color: #1f2a21;
            font-size: 1.15rem;
            line-height: 1.3;
            font-weight: 600;
            margin-bottom: 0.55rem;
        }
        .repository-highlight-copy {
            color: #5a6358;
            font-size: 0.95rem;
            line-height: 1.68;
            margin-bottom: 0.85rem;
        }
        .repository-highlight-meta {
            color: #72776f;
            font-size: 0.82rem;
            line-height: 1.55;
        }
        .repository-teaser-shell,
        .repository-detail-shell,
        .repository-side-note {
            background: rgba(255, 252, 247, 0.9);
            border: 1px solid rgba(124, 116, 103, 0.14);
            border-radius: 22px;
            padding: 1.1rem 1.15rem;
            box-shadow: 0 14px 28px rgba(78, 72, 61, 0.04);
        }
        .repository-teaser-title {
            color: #1f2a21;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.45rem;
        }
        .repository-teaser-copy {
            color: #5f655e;
            line-height: 1.7;
            margin-bottom: 0.8rem;
        }
        .repository-teaser-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
        }
        .repository-teaser-pills span {
            background: rgba(111, 138, 111, 0.1);
            color: #4e624e;
            border: 1px solid rgba(111, 138, 111, 0.16);
            border-radius: 999px;
            padding: 0.24rem 0.62rem;
            font-size: 0.78rem;
            font-weight: 500;
        }
        .repository-side-note {
            color: #5f655e;
            line-height: 1.7;
            margin-bottom: 0.9rem;
        }
        @media (max-width: 900px) {
            a.home-card,
            a.home-card:visited,
            a.home-card:hover,
            a.home-card:active {
                min-height: 198px;
            }
            .analytics-title {
                font-size: 2rem;
            }
            .repository-hero-title {
                font-size: 1.6rem;
            }
            .repository-activity-row {
                align-items: flex-start;
            }
            .analytics-history-card {
                min-height: auto;
                margin-top: 0.75rem;
            }
            .analytics-history-scroll {
                max-height: 320px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(
        """
        <script>
        const applyDangerButtonStyles = () => {
          const buttons = window.parent.document.querySelectorAll('button');
          buttons.forEach((button) => {
            const label = (button.innerText || '').trim().toLowerCase();
            const isDeleteButton = label.includes('delete custom exercise')
              || label.includes('delete permanently')
              || label.includes('confirm delete');

            if (!isDeleteButton) {
              return;
            }

            button.style.background = '#f4c7c3';
            button.style.borderColor = '#e8a29b';
            button.style.color = '#6f1d1b';
          });
        };

        applyDangerButtonStyles();

        const observer = new MutationObserver(() => applyDangerButtonStyles());
        observer.observe(window.parent.document.body, { childList: true, subtree: true });
        </script>
        """,
        height=0,
        width=0,
    )
