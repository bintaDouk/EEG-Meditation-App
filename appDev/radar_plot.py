
"""
Code for creating radar plot to visualize meditation session data.

To be implemented:
- Function to calculate radar values based on session data and own metrics
- Function to determine radar categories based on session data and user input (new categories can be added by user)
- Improve radar plot with visuals (dark theme, better colors, etc.)
- Function to store radar plot history and interface to select previous sessions and display corresponding radar plot

"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import os
from datetime import datetime

# ── Constants ─────────────────────────────────────────────────────────────────

HISTORY_FILE = "meditation_history.json"

DEFAULT_EXERCISES = [
    "Tibetan Relaxing",
    "Breathing Focus",
    "Body Scan",
    "Loving-kindness",
    "Visualization",
    "Open Awareness",
]

THEME = {
    "bg":     "#0d1b2a",
    "panel":  "#1a2d42",
    "grid":   "#2e4460",
    "accent": "#4dabf7",
    "prev":   "#a9e34b",
    "text":   "#e0eaf4",
    "muted":  "#6b8cae",
}

# ── Persistence ───────────────────────────────────────────────────────────────

def load_data() -> dict:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {
        "exercises": list(DEFAULT_EXERCISES),
        "averages":  {},
        "counts":    {},
        "sessions":  [],
    }


def save_data(data: dict) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_session(exercise: str, score: float, duration_min: int):
    data = load_data()
    prev_averages = dict(data["averages"])

    n = data["counts"].get(exercise, 0)
    old_avg = data["averages"].get(exercise, 0.0)
    new_avg = (old_avg * n + score) / (n + 1)

    data["counts"][exercise]   = n + 1
    data["averages"][exercise] = round(new_avg, 4)
    data["sessions"].append({
        "exercise":     exercise,
        "score":        round(score, 4),
        "duration_min": duration_min,
        "ts":           datetime.now().isoformat(),
    })

    save_data(data)
    return prev_averages, data["averages"]


def add_exercise(name: str) -> None:
    data = load_data()
    if name and name not in data["exercises"]:
        data["exercises"].append(name)
        save_data(data)

# ── Scoring placeholder ───────────────────────────────────────────────────────

def score_from_eeg(exercise: str, duration_min: int) -> float:
    """TODO: replace with real EEG ML pipeline."""
    return float(np.random.beta(3, 2))


# ── Plot ──────────────────────────────────────────────────────────────────────

def radar_plot(
    exercises:     list,
    averages:      dict,
    prev_averages: dict = None,
    title:         str  = "",
):
    N = len(exercises)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    def close(lst): return lst + lst[:1]

    vals = [averages.get(ex, 0.0) for ex in exercises]
    angs = close(angles)
    vs   = close(vals)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(THEME["bg"])
    ax.set_facecolor(THEME["bg"])

    for r in np.linspace(0.2, 1.0, 5):
        ax.plot(np.linspace(0, 2 * np.pi, 300), [r] * 300,
                color=THEME["grid"], linewidth=0.6, alpha=0.45)
    for ang in angles:
        ax.plot([ang, ang], [0, 1], color=THEME["grid"],
                linewidth=0.6, alpha=0.45)

    handles = []
    if prev_averages is not None:
        pv = close([prev_averages.get(ex, 0.0) for ex in exercises])
        ax.plot(angs, pv, color=THEME["prev"], linewidth=1.8,
                linestyle="--", alpha=0.6, zorder=2)
        ax.fill(angs, pv, color=THEME["prev"], alpha=0.08, zorder=1)
        handles.append(mpatches.Patch(color=THEME["prev"], alpha=0.7,
                                      label="Before session"))

    ax.plot(angs, vs,  color=THEME["accent"], linewidth=2.2, zorder=4)
    ax.fill(angs, vs,  color=THEME["accent"], alpha=0.22, zorder=3)
    ax.scatter(angles, vals, s=50, color=THEME["accent"],
               edgecolors=THEME["bg"], linewidths=1.4, zorder=5)
    handles.append(mpatches.Patch(color=THEME["accent"], alpha=0.7,
                                  label="After session"))

    ax.set_xticks(angles)
    ax.set_xticklabels(exercises, color=THEME["text"],
                       fontsize=9, fontfamily="monospace")
    ax.tick_params(pad=12)
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    ax.spines["polar"].set_visible(False)
    ax.grid(False)

    if prev_averages is not None:
        ax.legend(handles=handles, loc="upper right",
                  bbox_to_anchor=(1.3, 1.15),
                  framealpha=0, labelcolor=THEME["text"], fontsize=8.5)

    if title:
        ax.set_title(title, color=THEME["muted"],
                     fontsize=9, pad=20, fontfamily="monospace")

    fig.tight_layout()
    return fig


# ── Data management pannel ────────────────────────────────────────────────────────────────
def reset_all_logs():
    data = load_data()
    data["averages"] = {}
    data["counts"] = {}
    data["sessions"] = []
    save_data(data)


def delete_exercise(name: str):
    data = load_data()

    if name in data["exercises"]:
        data["exercises"].remove(name)

    data["averages"].pop(name, None)
    data["counts"].pop(name, None)

    data["sessions"] = [
        s for s in data["sessions"] if s["exercise"] != name
    ]

    save_data(data)

# ── Streamlit app ─────────────────────────────────────────────────────────────

def _css():
    st.markdown(f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;500&display=swap');
      html, body, [class*="css"] {{
          background-color: {THEME["bg"]};
          color: {THEME["text"]};
          font-family: 'Inter', sans-serif;
      }}
      h1, h2, h3 {{ font-family: 'Share Tech Mono', monospace; color: {THEME["accent"]}; }}
      .stButton > button {{
          background: {THEME["panel"]};
          color: {THEME["accent"]};
          border: 1px solid {THEME["accent"]};
          border-radius: 4px;
          font-family: 'Share Tech Mono', monospace;
      }}
      .stButton > button:hover {{
          background: {THEME["accent"]};
          color: {THEME["bg"]};
      }}
      .block-container {{ padding-top: 2rem; }}
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Meditation Radar", layout="wide", page_icon="🧘")
    _css()
    st.title("Meditation Radar - OSM")

    if "comparison" not in st.session_state:
        st.session_state.comparison = None

    data = load_data()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("Log a session")
        exercise = st.selectbox("Exercise", data["exercises"])
        duration = st.slider("Duration (min)", 1, 90, 20)

        if st.button("✅  Complete session", use_container_width=True):
            score = score_from_eeg(exercise, duration)
            prev_avg, new_avg = log_session(exercise, score, duration)
            st.session_state.comparison = (prev_avg, new_avg, exercise, score)
            st.rerun()

        st.divider()
        st.subheader("Add exercise")
        new_ex = st.text_input("New exercise name")
        if st.button("➕  Add", use_container_width=True) and new_ex:
            add_exercise(new_ex)
            st.rerun()

    
        st.divider()
        st.subheader("⚙️ Data Management")

        # Reload data so UI is always fresh
        data = load_data()

        # ── RESET SECTION ─────────────────────────────
        with st.expander("Reset all history", expanded=False):
            st.warning("This will permanently delete all sessions and averages.")

            confirm_reset = st.checkbox("I understand this cannot be undone")

            if st.button("Reset everything", use_container_width=True):
                if confirm_reset:
                    reset_all_logs()
                    st.success("All history reset.")
                    st.rerun()
                else:
                    st.error("Please confirm reset first.")

        # ── DELETE EXERCISE SECTION ───────────────────
        with st.expander("Delete an exercise", expanded=False):
            if data["exercises"]:
                exercise_to_delete = st.selectbox(
                    "Select exercise to delete",
                    data["exercises"]
                )

                # show impact preview
                sessions_count = len([
                    s for s in data["sessions"]
                    if s["exercise"] == exercise_to_delete
                ])
                avg = data["averages"].get(exercise_to_delete, 0)

                st.info(
                    f"Sessions: {sessions_count} | "
                    f"Avg score: {avg:.2f}"
                )

                confirm_delete = st.checkbox("Confirm deletion")

                if st.button("Delete exercise", use_container_width=True):
                    if confirm_delete:
                        delete_exercise(exercise_to_delete)
                        st.success(f"Deleted '{exercise_to_delete}'")
                        st.rerun()
                    else:
                        st.error("Please confirm deletion first.")
            else:
                st.info("No exercises to delete.")

                
    # ── Main area ─────────────────────────────────────────────────────────────
    data = load_data()

    if st.session_state.comparison:
        prev_avg, new_avg, exercise, score = st.session_state.comparison

        st.subheader(f"Session complete — {exercise}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Before**")
            st.pyplot(radar_plot(data["exercises"], prev_avg,
                                 title="before this session"),
                      use_container_width=True)
        with col2:
            st.markdown("**After**")
            st.pyplot(radar_plot(data["exercises"], new_avg,
                                 title="after this session"),
                      use_container_width=True)

        if st.button("← Back to overview"):
            st.session_state.comparison = None
            st.rerun()

    else:
        col_radar, col_log = st.columns([1.1, 0.9], gap="large")

        with col_radar:
            st.subheader("Your radar")
            if not data["averages"]:
                st.info("No sessions logged yet. Complete your first session →")
            st.pyplot(radar_plot(data["exercises"], data["averages"]),
                      use_container_width=True)

        with col_log:
            st.subheader("Session log")
            sessions = data["sessions"]
            if not sessions:
                st.info("Sessions will appear here.")
            else:
                for s in reversed(sessions[-30:]):
                    ts = s["ts"][:16].replace("T", " ")
                    ex_sessions = [x for x in sessions if x["exercise"] == s["exercise"]]
                    delta_str = ""
                    if len(ex_sessions) >= 2:
                        diff = ex_sessions[-1]["score"] - ex_sessions[-2]["score"]
                        delta_str = f" {'↑' if diff >= 0 else '↓'}{abs(diff):.2f}"
                    st.markdown(
                        f"`{ts}` &nbsp; **{s['exercise']}** &nbsp;"
                        f"`{s['duration_min']} min` &nbsp; score `{s['score']:.2f}`{delta_str}",
                        unsafe_allow_html=True,
                    )

            if data["averages"]:
                st.subheader("Running averages")
                for ex in data["exercises"]:
                    avg = data["averages"].get(ex)
                    if avg is None:
                        continue
                    n   = data["counts"].get(ex, 0)
                    bar = int(avg * 20)
                    st.markdown(
                        f"`{ex:<22}` `{'█'*bar}{'░'*(20-bar)}`"
                        f"`{avg:.2f}`  \n"
                        f"_{n} session{'s' if n!=1 else ''}_"



)


if __name__ == "__main__":
    main()