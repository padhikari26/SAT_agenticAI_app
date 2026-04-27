"""
════════════════════════════════════════════════════════════════
   SAT GENIUS — Agentic AI SAT Preparation Platform
   Streamlit · Groq · Agentic RAG · Adaptive Learning
════════════════════════════════════════════════════════════════
"""
import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="SAT Prep App",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    }
)


# ── Global CSS ──────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ---- VARIABLES ---- */
:root {
  --bg-secondary: rgba(255, 255, 255, 0.85);
  --bg-tertiary:  rgba(255, 255, 255, 0.95);
  --text-primary: #1e293b;
  --text-secondary: #475569;
  --accent-primary: #3498db;
  --accent-secondary: #34495e;
  --border-light: #d5d8dc;
}

/* ---- GLOBAL ---- */
html, body, [class*="css"] { 
  font-family:'Inter',sans-serif; 
  color:var(--text-primary); 
}

.stApp {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}

/* ---- FIX SIDEBAR VISIBILITY ---- */
section[data-testid="stSidebar"] {
  background: #009933 !important;
  color: white !important;
  width: 260px !important;
}

/* Only target text, not everything */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
  color: white !important;
}

/* Optional: soften sections */
section[data-testid="stSidebar"] hr {
  border-color: rgba(255,255,255,0.2) !important;
}

/* ---- FIX MAIN CONTENT ---- */
.block-container {
  max-width: 1000px;
  margin: auto;
  padding-top: 2rem;
  padding-left: 2rem;
  padding-right: 2rem;
}

/* ---- HEADINGS ---- */
h1, h2, h3 {
  font-family:'Inter',sans-serif!important;
  color:var(--text-primary)!important;
}

h1 {
  text-align: center !important;
  font-size: 2rem !important;
}

/* ---- BUTTONS ---- */
.stButton>button {
  border-radius:8px!important;
  background:var(--accent-primary)!important;
  color:white!important;
  padding:0.6rem 1.2rem!important;
}

.stButton>button:hover {
  background:var(--accent-secondary)!important;
}

/* ---- INPUTS ---- */
.stTextInput input,
.stTextArea textarea {
  background:var(--bg-secondary)!important;
  border:1px solid var(--border-light)!important;
  border-radius:8px!important;
  padding:0.6rem!important;
}

/* ---- CARDS (KEEP SIMPLE) ---- */
.genius-card {
  background: var(--bg-secondary);
  border-radius:12px;
  padding:1.2rem;
  border:1px solid var(--border-light);
}

/* ---- CLEAN UI ---- */
#MainMenu, footer {
  visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ── Pages list ──────────────────────────────────────────────────────────
PAGES = [
    "🏠 Dashboard",
    "🧠 AI Tutor",
    "📝 Practice",
    "📚 Concepts",
    "🎴 Flashcards",
    "🏆 Mock Test",
    "📊 Analytics",
    "🗺️ Study Plan",
    "⚙️ Settings",
]


# ── Session state ───────────────────────────────────────────────────────
def init_state():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    defaults = {
        "groq_api_key": os.getenv("GROQ_API_KEY", ""),
        "user_name": "",
        "onboarded": False,
        "current_page": "🏠 Dashboard",
        "page_index": 0,
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
def render_sidebar():
    with st.sidebar:

        # ── Brand Header ─────────────────────────────
        st.markdown("""
        <div style="padding:1.2rem;text-align:center;border-bottom:1px solid rgba(255,255,255,0.15);margin-bottom:1rem;">
          <div style="font-family:'Inter',sans-serif;font-size:1.2rem;font-weight:700;color:#ffffff;">
            SAT Prep
          </div>
          <div style="font-size:.65rem;color:rgba(236,240,241,0.7);
                      letter-spacing:.08em;text-transform:uppercase;">
            Learning Platform
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Status ─────────────────────────────
        status = "Connected" if st.session_state.groq_api_key else "Disconnected"
        color = "#27ae60" if status == "Connected" else "#e74c3c"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                    border-radius:8px;padding:8px 10px;font-size:.7rem;color:{color};
                    margin:0 0.8rem 1rem;text-align:center;font-weight:600;">
          System: {status}
        </div>
        """, unsafe_allow_html=True)

        # ── User Stats ─────────────────────────────
        if st.session_state.onboarded:
            total = st.session_state.math_score + st.session_state.rw_score
            acc = (st.session_state.correct_answers / st.session_state.total_questions * 100
                   if st.session_state.total_questions > 0 else 0)

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                        border-radius:10px;padding:0.9rem;margin:0 0.8rem 1.2rem;color:#ffffff;">
              
              <div style="font-weight:600;font-size:.85rem;margin-bottom:.6rem;">
                {st.session_state.user_name}
              </div>

              <div style="display:flex;justify-content:space-between;font-size:.72rem;margin-bottom:4px;">
                <span>Score</span><span>{total}</span>
              </div>

              <div style="display:flex;justify-content:space-between;font-size:.72rem;margin-bottom:4px;">
                <span>Accuracy</span><span>{acc:.0f}%</span>
              </div>

              <div style="display:flex;justify-content:space-between;font-size:.72rem;">
                <span>XP</span><span>{st.session_state.xp_points}</span>
              </div>

            </div>
            """, unsafe_allow_html=True)

        # ── Navigation ─────────────────────────────
        st.markdown("""
        <div style="padding:0.5rem 1rem;color:rgba(255,255,255,0.6);
                    font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;">
          Navigation
        </div>
        """, unsafe_allow_html=True)

        current = st.session_state.current_page

        for i, page in enumerate(PAGES):
            is_active = page == current

            if st.button(
                page,
                key=f"nav_{i}",
                use_container_width=True
            ):
                go_to_page(page)

        # ── Footer ─────────────────────────────
        st.markdown(f"""
        <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.1);
                    font-size:.65rem;color:rgba(236,240,241,0.5);text-align:center;">
          Day {st.session_state.streak_days} · {st.session_state.total_questions} solved
        </div>
        """, unsafe_allow_html=True)


# ── Onboarding ──────────────────────────────────────────────────────────
def render_onboarding():
    st.markdown("""
    <div style="max-width:680px;margin:2rem auto 0;text-align:center;">
      <div style="font-family:'Roboto Mono',monospace;font-size:2.5rem;font-weight:700;line-height:1;
                  color:#2c3e50;margin-bottom:0.3rem;">
        SAT Prep App
      </div>
      <div style="font-size:1rem;color:#2c3e50;margin-bottom:.3rem;font-family:'Roboto Mono',monospace;">
        Comprehensive SAT preparation platform
      </div>
      <div style="font-family:'Roboto Mono',monospace;font-size:.7rem;color:#5a6c7d;
                  letter-spacing:.08em;text-transform:uppercase;margin-bottom:2rem;">
        Adaptive Learning
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
       # st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("### Personalize Your Prep")

        name = st.text_input("Your name", placeholder="e.g., Alex Chen")

        a, b = st.columns(2)
        with a:
            target = st.slider("Target SAT Score", 800, 1600, 1400, 10)
        with b:
            level = st.selectbox(
                "Current Level",
                ["Beginner (<900)", "Intermediate (900–1100)",
                 "Advanced (1100–1300)", "Expert (1300+)"],
            )

        focus = st.multiselect(
            "Focus Areas",
            ["Math · Algebra", "Math · Advanced Math",
             "Math · Problem Solving & Data", "Math · Geometry & Trig",
             "Reading · Information & Ideas", "Reading · Craft & Structure",
             "Writing · Standard English", "Writing · Expression of Ideas"],
            default=["Math · Algebra", "Reading · Information & Ideas"],
            max_selections=4,
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Start Learning", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Please enter your name.")
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
                st.session_state.current_page = "🏠 Dashboard"
                st.session_state.page_index = 0
                st.session_state.onboarded = True
                st.rerun()


# ── Router ──────────────────────────────────────────────────────────────
# ── Navigation helpers ─────────────────────────────────────────────────
def go_to_page(page_name):
    """Navigate to a specific page by name."""
    if page_name in PAGES:
        st.session_state.current_page = page_name
        st.session_state.page_index = PAGES.index(page_name)
        st.rerun()


def route():
    page = st.session_state.current_page
    try:
        if page == "🏠 Dashboard":
            import dashboard; dashboard.render()
        elif page == "🧠 AI Tutor":
            import ai_tutor; ai_tutor.render()
        elif page == "📝 Practice":
            import practice; practice.render()
        elif page == "📚 Concepts":
            import concepts; concepts.render()
        elif page == "🎴 Flashcards":
            import flashcards; flashcards.render()
        elif page == "🏆 Mock Test":
            import mock_test; mock_test.render()
        elif page == "📊 Analytics":
            import analytics; analytics.render()
        elif page == "🗺️ Study Plan":
            import study_plan; study_plan.render()
        elif page == "⚙️ Settings":
            import settings; settings.render()
        else:
            import dashboard; dashboard.render()
    except Exception as e:
        st.error(f"Page error: {e}")
        st.exception(e)

def main():
    inject_css()
    init_state()

    # ✅ ALWAYS render sidebar
    render_sidebar()

    # Main content
    if not st.session_state.onboarded:
        render_onboarding()
    else:
        route()

if __name__ == "__main__":
    main()
