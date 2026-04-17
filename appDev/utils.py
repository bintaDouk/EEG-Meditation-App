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

EXERCISE_DETAILS = {
    "Tibetan Relaxing": {
        "category": "Restoration",
        "summary": "A soft settling practice that eases the body before deeper stillness.",
        "description": (
            "Tibetan Relaxing invites the body to unclench first so the mind can follow. "
            "It works well at the start of the day, before sleep, or after an intense session."
        ),
        "how_to": [
            "Let the shoulders drop and take a few slower exhalations than inhalations.",
            "Scan the face, jaw, chest, and belly for hidden tension and release it gently.",
            "Stay with the feeling of softness instead of trying to force concentration.",
        ],
    },
    "Breathing Focus": {
        "category": "Attention",
        "summary": "A classic anchor practice built around the rhythm of the breath.",
        "description": (
            "Breathing Focus trains steady attention by returning awareness to inhale and exhale. "
            "It is simple, reliable, and a strong baseline practice for tracking consistency."
        ),
        "how_to": [
            "Choose one breath location such as the nostrils, chest, or belly.",
            "Count breaths or silently note in and out when attention drifts.",
            "Each return to the breath counts as part of the practice, not a mistake.",
        ],
    },
    "Body Scan": {
        "category": "Awareness",
        "summary": "A grounded practice for noticing sensation from head to toe.",
        "description": (
            "Body Scan helps widen awareness and reconnect attention with physical sensation. "
            "It is useful when the mind feels restless, scattered, or overly verbal."
        ),
        "how_to": [
            "Move attention through the body slowly, region by region.",
            "Notice warmth, tingling, pressure, or numbness without needing to change anything.",
            "If the mind races, return to the last body area you clearly remember.",
        ],
    },
    "Loving-kindness": {
        "category": "Compassion",
        "summary": "A heart-centered technique that grows goodwill toward self and others.",
        "description": (
            "Loving-kindness uses short phrases and emotional intention to cultivate warmth. "
            "It can balance highly effortful concentration with gentleness and connection."
        ),
        "how_to": [
            "Begin with yourself using simple phrases such as may I be safe and at ease.",
            "Expand the phrases to someone you care about, then to neutral people, then wider circles.",
            "Focus more on sincerity than on producing a specific emotion.",
        ],
    },
    "Visualization": {
        "category": "Imagery",
        "summary": "A guided inner-image technique for calm, direction, and emotional tone.",
        "description": (
            "Visualization pairs attention with mental imagery, often using a place, light, or symbolic scene. "
            "It can support motivation, emotional regulation, and a sense of intention."
        ),
        "how_to": [
            "Choose one image and keep it stable rather than switching scenes repeatedly.",
            "Layer in sound, color, texture, or temperature to make the image feel vivid.",
            "If the image fades, return to the emotional quality you want it to evoke.",
        ],
    },
    "Open Awareness": {
        "category": "Observation",
        "summary": "A spacious practice that notices thoughts, sensations, and sounds as they arise.",
        "description": (
            "Open Awareness broadens attention beyond one anchor and invites experience to come and go. "
            "It is useful once basic stability is present and you want a less effortful style of monitoring."
        ),
        "how_to": [
            "Let sounds, sensations, and thoughts enter awareness without chasing any of them.",
            "Notice the changing field of experience instead of locking onto one object.",
            "When you get absorbed, gently reopen to the whole moment again.",
        ],
    },
}

THEME = {
    "bg":     "#f8f4ec",
    "panel":  "#fbf7ef",
    "grid":   "#ddd7ca",
    "accent": "#6f8a6f",
    "prev":   "#b9c7ad",
    "text":   "#1f2a21",
    "muted":  "#7a7468",
}

# ── Persistence ───────────────────────────────────────────────────────────────

def load_data() -> dict:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            data = json.load(f)
    else:
        data = {
            "exercises": list(DEFAULT_EXERCISES),
            "averages":  {},
            "counts":    {},
            "sessions":  [],
            "custom_exercise_details": {},
        }

    data.setdefault("exercises", list(DEFAULT_EXERCISES))
    data.setdefault("averages", {})
    data.setdefault("counts", {})
    data.setdefault("sessions", [])
    data.setdefault("custom_exercise_details", {})
    return data


def save_data(data: dict) -> None:
    data.setdefault("custom_exercise_details", {})
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _default_data() -> dict:
    return {
        "exercises": list(DEFAULT_EXERCISES),
        "averages":  {},
        "counts":    {},
        "sessions":  [],
        "custom_exercise_details": {},
    }


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


def add_exercise(
    name: str,
    description: str = "",
    how_to: list[str] | None = None,
    guide_data: str = "",
    precision_criteria: str = "",
) -> None:
    data = load_data()
    clean_name = name.strip()
    if not clean_name:
        return

    if clean_name not in data["exercises"]:
        data["exercises"].append(clean_name)

    if (
        description.strip()
        or (how_to and any(step.strip() for step in how_to))
        or guide_data.strip()
        or precision_criteria.strip()
    ):
        steps = [step.strip() for step in (how_to or []) if step.strip()]
        data["custom_exercise_details"][clean_name] = {
            "category": "Custom",
            "summary": description.strip() or "A custom meditation exercise added by the user.",
            "description": description.strip() or f"{clean_name} is a custom meditation exercise.",
            "how_to": steps or [
                "Follow the custom instructions you saved for this technique.",
            ],
            "guide_data": guide_data.strip(),
            "precision_criteria": precision_criteria.strip(),
            "created_at": datetime.now().isoformat(),
            "is_custom": True,
        }

    save_data(data)


def get_exercise_details(exercise: str) -> dict:
    data = load_data()
    custom_metadata = data["custom_exercise_details"].get(exercise)
    if custom_metadata is not None:
        return {
            **custom_metadata,
            "created_at": custom_metadata.get("created_at"),
        }

    metadata = EXERCISE_DETAILS.get(exercise)
    if metadata is not None:
        return {
            **metadata,
            "guide_data": metadata.get("guide_data", ""),
            "precision_criteria": metadata.get("precision_criteria", ""),
            "is_custom": False,
        }
    return {
        "category": "Technique",
        "summary": "A saved meditation exercise in your library.",
        "description": (
            f"{exercise} is available in your library. Add fuller guidance here later as you refine "
            "the technique and collect more user-specific insight."
        ),
        "how_to": [
            "Settle into a comfortable posture and begin with a few slower breaths.",
            "Follow the core instructions of this technique with a light but steady attention.",
            "After practice, note what felt effective so the method can evolve over time.",
        ],
        "guide_data": "",
        "precision_criteria": "",
        "is_custom": False,
    }


def get_available_exercises() -> list[str]:
    return load_data()["exercises"]


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
    data["custom_exercise_details"].pop(name, None)

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
                       fontsize=9)
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
                     fontsize=9, pad=20)

    fig.tight_layout()
    return fig


# ── Streamlit app ─────────────────────────────────────────────────────────────

def _css():
    st.markdown(f"""
    <style>
      html, body, [class*="css"] {{
          background-color: {THEME["bg"]};
          color: {THEME["text"]};
          font-family: sans-serif;
      }}
      h1, h2, h3 {{ color: {THEME["text"]}; }}
      .stButton > button {{
          background: {THEME["panel"]};
          color: {THEME["text"]};
          border: 1px solid rgba(124, 116, 103, 0.18);
          border-radius: 999px;
      }}
      .stButton > button:hover {{
          background: {THEME["panel"]};
          color: {THEME["text"]};
      }}
      .block-container {{ padding-top: 2rem; }}
    </style>
    """, unsafe_allow_html=True)
