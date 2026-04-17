import json

import streamlit as st
import streamlit.components.v1 as components

from session_runtime import clear_session_runtime, get_session_runtime


def _format_clock(total_seconds: int) -> str:
    minutes, seconds = divmod(max(0, total_seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


def _render_live_session_panel(session_config: dict, runtime: dict):
    payload = {
        "sessionRemaining": runtime["session_remaining_sec"],
        "sessionTotal": runtime["session_duration_sec"],
        "mode": session_config["mode"],
        "durationLabel": session_config["duration_label"],
    }

    component_html = f"""
    <div id="osm-session-player" style="
        border:1px solid #d7dacd;
        border-radius:24px;
        overflow:hidden;
        background:#f7f4ec;
        font-family: 'Segoe UI', sans-serif;
    ">
        <div id="osm-player-screen" style="
            background:#243126;
            color:#fff6ea;
            padding:42px 38px 36px;
        ">
            <div id="osm-player-badge" style="
                font-size:12px;
                letter-spacing:0.18em;
                text-transform:uppercase;
                color:#efe3cc;
                margin-bottom:18px;
            ">Session live</div>
            <div id="osm-player-time" style="
                font-size:68px;
                line-height:1;
                font-weight:700;
                margin-bottom:18px;
            ">{_format_clock(runtime["session_remaining_sec"])}</div>
            <div id="osm-player-copy" style="
                font-size:18px;
                line-height:1.5;
                color:#f6ead8;
            ">Your session is now in progress.</div>
        </div>
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:16px;
            padding:14px 22px;
            background:#fbf8f1;
            color:#6d7068;
            font-size:14px;
        ">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="
                    width:12px;
                    height:12px;
                    border-radius:999px;
                    display:inline-block;
                    background:#d76d45;
                    flex-shrink:0;
                "></span>
                <span id="osm-player-label">Live session</span>
            </div>
            <div id="osm-player-meta">{_format_clock(runtime["session_duration_sec"] - runtime["session_remaining_sec"])} / {_format_clock(runtime["session_duration_sec"])}</div>
        </div>
    </div>
    <script>
    const payload = {json.dumps(payload)};

    const timeEl = document.getElementById("osm-player-time");
    const badgeEl = document.getElementById("osm-player-badge");
    const copyEl = document.getElementById("osm-player-copy");
    const labelEl = document.getElementById("osm-player-label");
    const metaEl = document.getElementById("osm-player-meta");

    let sessionRemaining = Number(payload.sessionRemaining || 0);
    const sessionTotal = Math.max(1, Number(payload.sessionTotal || 0));
    const mode = payload.mode || "Silent";
    const durationLabel = payload.durationLabel || "session";

    function fmt(totalSeconds) {{
        const safe = Math.max(0, totalSeconds);
        const minutes = String(Math.floor(safe / 60)).padStart(2, "0");
        const seconds = String(safe % 60).padStart(2, "0");
        return `${{minutes}}:${{seconds}}`;
    }}

    function render() {{
        if (sessionRemaining > 0) {{
            const elapsed = sessionTotal - sessionRemaining;
            badgeEl.textContent = mode === "Guided" ? "Guided session" : "Session live";
            timeEl.textContent = fmt(sessionRemaining);
            copyEl.textContent = mode === "Guided"
                ? `A ${{durationLabel}} guided session is now in progress.`
                : `Your ${{durationLabel}} session is now in progress.`;
            labelEl.textContent = mode === "Guided" ? "Guided stream" : "Live session";
            metaEl.textContent = `${{fmt(elapsed)}} / ${{fmt(sessionTotal)}}`;
            return;
        }}

        badgeEl.textContent = "Session complete";
        timeEl.textContent = "00:00";
        copyEl.textContent = "Take a quiet moment before moving on.";
        labelEl.textContent = "Complete";
        metaEl.textContent = `${{fmt(sessionTotal)}} / ${{fmt(sessionTotal)}}`;
    }}

    render();

    window.setInterval(() => {{
        if (sessionRemaining > 0) {{
            sessionRemaining -= 1;
        }}
        render();
    }}, 1000);
    </script>
    """

    components.html(component_html, height=320)


def _render_guided_media_panel(runtime: dict):
    total = max(1, runtime["session_duration_sec"])
    elapsed = total - runtime["session_remaining_sec"]
    progress = min(1.0, max(0.0, elapsed / total))

    st.markdown(
        """
        <div class="guided-media-shell">
            <div class="guided-media-title">Guided session media</div>
            <div class="guided-media-copy">
                Placeholder guided media panel. This area is ready for a local video
                asset when one is added to the app.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(progress, text=f"Guided media progress {_format_clock(elapsed)}")


def render_session_run_view(go_to):
    session_config = st.session_state.get("session_config")
    runtime = get_session_runtime()

    if not session_config or not runtime:
        clear_session_runtime()
        st.session_state["session_started"] = False
        go_to("planner")
        st.rerun()

    st.title(session_config["practice"])
    st.caption(f"{session_config['mode']} - {session_config['duration_label']}")

    _render_live_session_panel(session_config, runtime)

    info_left, info_right = st.columns(2)
    with info_left:
        st.markdown(f"**Practice:** {session_config['practice']}")
        st.markdown(f"**Mode:** {session_config['mode']}")
        st.markdown(f"**Duration:** {session_config['duration_label']}")
    with info_right:
        st.markdown(
            f"**EEG:** {'Connected' if session_config['devices']['eeg'] else 'Not connected'}"
        )
        st.markdown(
            f"**Band:** {'Connected' if session_config['devices']['band'] else 'Not connected'}"
        )

    if session_config["mode"] == "Guided":
        st.divider()
        _render_guided_media_panel(runtime)

    st.divider()
    if st.button("Stop session", use_container_width=True, key="stop_session_primary"):
        clear_session_runtime()
        st.session_state["session_started"] = False
        go_to("planner")
        st.rerun()
