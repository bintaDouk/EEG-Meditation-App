from datetime import datetime
import json
import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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