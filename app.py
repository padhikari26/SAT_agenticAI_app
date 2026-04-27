"""
SAT Prep — main entry point
Streamlit app, modular page routing.
"""
import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="SAT Prep",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Global CSS ──────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Core theme (high contrast grayscale) ── */
:root {
  --bg: #ffffff;
  --bg-alt: #f5f5f5;

  --text: #111111;
  --text-muted: #444444;   /* darker for readability */
  --text-faint: #777777;

  --border: #dddddd;
  --border-strong: #999999;

  --sidebar-bg: #0a0a0a;
  --sidebar-hover: #1a1a1a;
  --sidebar-active: #ffffff;
  --sidebar-text: #e5e5e5;

  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', sans-serif;
}

html, body, [class*="css"] {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  border-right: 1px solid #222 !important;
}

[data-testid="stSidebar"] * {
  color: var(--sidebar-text) !important;
}

/* Nav buttons */
[data-testid="stSidebar"] .stButton>button {
  background: transparent !important;
  border: none !important;
  color: #bbbbbb !important;
  text-align: left !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
  padding: 0.55rem 0.9rem !important;
}

/* Hover */
[data-testid="stSidebar"] .stButton>button:hover {
  background: var(--sidebar-hover) !important;
  color: #ffffff !important;
}

/* ACTIVE PAGE (this is key fix) */
[data-testid="stSidebar"] .stButton>button:focus {
  background: var(--sidebar-active) !important;
  color: #000000 !important;
  outline: none !important;
}

/* ── Typography ── */
h1 {
  font-size: 1.6rem !important;
  font-weight: 600 !important;
  color: var(--text);
}

h2 {
  font-size: 1.25rem !important;
  font-weight: 500 !important;
}

h3 {
  font-size: 1.05rem !important;
  font-weight: 500 !important;
}

p, span, div {
  color: var(--text);
}

small, .caption {
  color: var(--text-muted) !important;
}

/* ── Buttons ── */
.stButton>button {
  background: #ffffff !important;
  color: #000000 !important;
  border: 1px solid #000000 !important;
  border-radius: 4px !important;
  font-size: 0.85rem !important;
}

.stButton>button:hover {
  background: #000000 !important;
  color: #ffffff !important;
}

/* ── Inputs ── */
input, textarea {
  border: 1px solid var(--border-strong) !important;
  border-radius: 4px !important;
  padding: 0.5rem !important;
  color: var(--text) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  padding: 0 !important;
}

[data-testid="stMetricLabel"] {
  font-size: 0.7rem !important;
  text-transform: uppercase !important;
  color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
  font-size: 1.5rem !important;
  font-family: var(--mono) !important;
  color: var(--text) !important;
}

/* ── Progress ── */
.stProgress > div > div > div {
  background: #000000 !important;
}

.stProgress > div > div {
  background: #e5e5e5 !important;
}

/* ── Divider ── */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.2rem 0;
}

/* ── Remove Streamlit chrome ── */
#MainMenu, footer, header {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ───────────────────────────────────────────────────────
def init_state():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    defaults = {
        "groq_api_key": os.getenv("GROQ_API_KEY", ""),
        "user_name": "",
        "onboarded": False,
        "current_page": "Dashboard",
        "math_score": 400,
        "rw_score": 400,
        "target_score": 1400,
        "total_questions": 0,
        "correct_answers": 0,
        "xp_points": 0,
        "streak_days": 1,
        "practice_history": [],
        "chat_history": [],
        "current_quiz": None,
        "quiz_index": 0,
        "quiz_answers": [],
        "flashcard_deck": [],
        "flashcard_index": 0,
        "weak_topics": [],
        "strong_topics": [],
        "focus_areas": [],
        "study_plan": "",
        "model_choice": "llama-3.1-8b-instant",
        "difficulty": "Medium",
        "mock_test_state": None,
        "ai_offline_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Sidebar ─────────────────────────────────────────────────────────────
PAGES = [
    "Dashboard",
    "Practice",
    "Tutor",
    "Concepts",
    "Flashcards",
    "Mock Test",
    "Analytics",
    "Study Plan",
    "Settings",
]


def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding:0 1rem 1rem;border-bottom:1px solid #27272a;">
          <div style="font-family:var(--mono);font-size:0.7rem;color:var(--sidebar-mute);
                      letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.2rem;">
            v1.0
          </div>
          <div style="font-family:var(--sans);font-size:1.2rem;font-weight:600;color:#ffffff;
                      letter-spacing:-0.01em;">
            SAT Prep
          </div>
          <div style="font-family:var(--mono);font-size:0.7rem;color:var(--sidebar-mute);
                      margin-top:0.25rem;">
            adaptive · structured
          </div>
        </div>
        """, unsafe_allow_html=True)

        # API status
        if st.session_state.groq_api_key:
            st.markdown("""
            <div style="padding:0.7rem 1rem 0;">
              <div class="status-pill status-ok">● api connected</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:0.7rem 1rem 0;">
              <div class="status-pill status-err">● api not configured</div>
            </div>
            """, unsafe_allow_html=True)

        # User stats
        if st.session_state.onboarded:
            total = st.session_state.math_score + st.session_state.rw_score
            acc = (st.session_state.correct_answers / st.session_state.total_questions * 100
                   if st.session_state.total_questions > 0 else 0)
            st.markdown(f"""
            <div style="padding:1rem;margin:0.8rem 1rem 0;background:#27272a;
                        border-radius:6px;border:1px solid #3f3f46;">
              <div style="font-family:var(--mono);font-size:0.72rem;
                          color:var(--sidebar-mute);text-transform:uppercase;
                          letter-spacing:0.05em;margin-bottom:0.5rem;">
                {st.session_state.user_name or 'user'}
              </div>
              <div class="sb-stat-row"><span>score</span><span>{total}</span></div>
              <div class="sb-stat-row"><span>accuracy</span><span>{acc:.0f}%</span></div>
              <div class="sb-stat-row"><span>solved</span><span>{st.session_state.total_questions}</span></div>
              <div class="sb-stat-row"><span>xp</span><span>{st.session_state.xp_points}</span></div>
            </div>
            """, unsafe_allow_html=True)

        # Navigation
        st.markdown(
            '<div class="sb-section"><div class="sb-label">navigation</div></div>',
            unsafe_allow_html=True
        )

        for p in PAGES:
            label = f"  {p.lower()}"
            # mark active page
            if st.session_state.current_page == p:
                label = f"› {p.lower()}"
            if st.button(label, use_container_width=True, key=f"nav_{p}"):
                st.session_state.current_page = p
                st.rerun()

        # Footer
        st.markdown(
            f'<div style="padding:1rem;border-top:1px solid #27272a;margin-top:1.5rem;'
            f'font-family:var(--mono);font-size:0.68rem;color:var(--sidebar-mute);">'
            f'day {st.session_state.streak_days} · {st.session_state.total_questions} solved'
            '</div>',
            unsafe_allow_html=True
        )


# ── Onboarding ──────────────────────────────────────────────────────────
def render_onboarding():
    st.markdown("""
    <div style="max-width:560px;margin:3rem auto 1.5rem;">
      <div style="font-family:var(--mono);font-size:0.72rem;color:var(--text-faint);
                  letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">
        setup · v1.0
      </div>
      <div style="font-family:var(--sans);font-size:2rem;font-weight:600;
                  color:var(--text);letter-spacing:-0.02em;margin-bottom:0.3rem;">
        SAT Prep
      </div>
      <div style="font-size:0.95rem;color:var(--text-mute);">
        Configure your profile to begin. Takes about 30 seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.markdown("**Profile**")
        name = st.text_input("Name", placeholder="e.g., Alex Chen")

        a, b = st.columns(2)
        with a:
            target = st.slider("Target score", 800, 1600, 1400, 10)
        with b:
            level = st.selectbox(
                "Current level",
                ["Beginner (<900)", "Intermediate (900–1100)",
                 "Advanced (1100–1300)", "Expert (1300+)"],
            )

        focus = st.multiselect(
            "Focus areas",
            ["Math · Algebra", "Math · Advanced Math",
             "Math · Problem Solving & Data", "Math · Geometry & Trig",
             "Reading · Information & Ideas", "Reading · Craft & Structure",
             "Writing · Standard English", "Writing · Expression of Ideas"],
            default=["Math · Algebra", "Reading · Information & Ideas"],
            max_selections=4,
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        if st.button("Continue →", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Name is required.")
            else:
                st.session_state.user_name = name.strip()
                st.session_state.target_score = target
                st.session_state.focus_areas = focus
                level_map = {
                    "Beginner (<900)": (380, 380),
                    "Intermediate (900–1100)": (480, 480),
                    "Advanced (1100–1300)": (580, 580),
                    "Expert (1300+)": (650, 650),
                }
                ms, rs = level_map[level]
                st.session_state.math_score = ms
                st.session_state.rw_score = rs
                st.session_state.xp_points = 100
                st.session_state.onboarded = True
                st.rerun()


# ── Router ──────────────────────────────────────────────────────────────
def route():
    page = st.session_state.current_page
    try:
        if page == "Dashboard":
            import dashboard; dashboard.render()
        elif page == "Tutor":
            import ai_tutor; ai_tutor.render()
        elif page == "Practice":
            import practice; practice.render()
        elif page == "Concepts":
            import concepts; concepts.render()
        elif page == "Flashcards":
            import flashcards; flashcards.render()
        elif page == "Mock Test":
            import mock_test; mock_test.render()
        elif page == "Analytics":
            import analytics; analytics.render()
        elif page == "Study Plan":
            import study_plan; study_plan.render()
        elif page == "Settings":
            import settings; settings.render()
        else:
            import dashboard; dashboard.render()
    except Exception as e:
        st.error(f"Page error: {e}")
        st.exception(e)


def main():
    inject_css()
    init_state()
    if not st.session_state.onboarded:
        render_onboarding()
    else:
        render_sidebar()
        route()


if __name__ == "__main__":
    main()