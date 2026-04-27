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

:root {
  --bg-main:      #000000;
  --bg-secondary: #000000;
  --bg-tertiary:  #f5f6f7;
  --sidebar-bg:   #ffffff;
  --sidebar-text: #000000;
  --text-primary: #ffffff;
  --text-secondary: #ffffff;
  --accent-primary: #3498db;
  --accent-secondary: #34495e;
  --success: #27ae60;
  --danger: #e74c3c;
  --border-light: #d5d8dc;
  --border-dark: #bdc3c7;
  --green: #27ae60;
  --rose: #e74c3c;
}

html, body, [class*="css"] { 
  font-family:'Inter',sans-serif; 
  color:var(--text-primary); 
  background:var(--bg-main);
}

.stApp {
  background:var(--bg-main);
}

[data-testid="stSidebar"] {
  background:linear-gradient(180deg, #2c3e50 0%, #34495e 100%)!important;
  border-right:1px solid rgba(255,255,255,0.1)!important;
  padding:1rem 0!important;
  position:sticky!important;
  top:0!important;
}

[data-testid="stSidebar"] > div:first-child {
  padding:0!important;
}

h1, h2, h3, h4, h5 {
  font-family:'Inter',sans-serif!important;
  color:var(--text-primary)!important;
  font-weight:600!important;
}

h1 { font-size:2rem!important; margin-bottom:0.5rem!important; }
h2 { font-size:1.5rem!important; }
h3 { font-size:1.1rem!important; }

.stButton>button {
  font-family:'Inter',sans-serif!important;
  font-weight:500!important;
  border-radius:8px!important;
  border:1px solid var(--border-light)!important;
  background:var(--accent-primary)!important;
  color:white!important;
  transition:all 0.2s ease!important;
  padding:0.6rem 1.2rem!important;
}

.stButton>button:hover {
  background:var(--accent-secondary)!important;
  border-color:var(--accent-secondary)!important;
  transform:translateY(-1px)!important;
  box-shadow:0 2px 8px rgba(52, 73, 94, 0.2)!important;
}

.stButton>button:disabled {
  background:#bdc3c7!important;
  border-color:#bdc3c7!important;
  opacity:0.6!important;
  cursor:not-allowed!important;
}

[data-testid="stBaseButton-secondary"] {
  background:var(--bg-secondary)!important;
  color:var(--text-primary)!important;
  border:1px solid var(--border-light)!important;
}

[data-testid="stBaseButton-secondary"]:hover {
  background:var(--bg-tertiary)!important;
  border-color:var(--text-secondary)!important;
}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input {
  background:var(--bg-secondary)!important;
  border:1px solid var(--border-light)!important;
  border-radius:8px!important;
  color:var(--text-primary)!important;
  font-family:'Inter',sans-serif!important;
  font-size:0.95rem!important;
  padding:0.7rem 1rem!important;
  transition:all 0.2s ease!important;
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
  border-color:var(--accent-primary)!important;
  box-shadow:0 0 0 3px rgba(52, 152, 219, 0.1)!important;
  outline:none!important;
}

[data-baseweb="select"]>div {
  background:var(--bg-secondary)!important;
  border-color:var(--border-light)!important;
  border-radius:8px!important;
}

[data-testid="metric-container"] {
  background:var(--bg-secondary);
  border:1px solid var(--border-light);
  border-radius:12px;
  padding:1.2rem;
  transition:all 0.2s ease;
}

[data-testid="metric-container"]:hover {
  border-color:var(--accent-primary);
  box-shadow:0 2px 8px rgba(52, 152, 219, 0.1);
}

[data-testid="stMetricLabel"] {
  font-family:'Inter',sans-serif!important;
  font-size:0.75rem!important;
  letter-spacing:0.05em!important;
  text-transform:uppercase!important;
  color:var(--text-secondary)!important;
  font-weight:600!important;
}

[data-testid="stMetricValue"] {
  font-family:'Inter',sans-serif!important;
  font-weight:700!important;
  color:var(--accent-primary)!important;
  font-size:1.8rem!important;
}

.stTabs [data-baseweb="tab-list"] {
  background:transparent!important;
  border-bottom:1px solid var(--border-light)!important;
  gap:0!important;
  padding:0!important;
}

.stTabs [data-baseweb="tab"] {
  background:transparent!important;
  color:var(--text-secondary)!important;
  font-family:'Inter',sans-serif!important;
  font-weight:500!important;
  border-radius:0!important;
  border:none!important;
  border-bottom:2px solid transparent!important;
  padding:0.8rem 1.2rem!important;
  transition:all 0.2s ease!important;
}

.stTabs [aria-selected="true"] {
  background:transparent!important;
  color:var(--accent-primary)!important;
  border-bottom:2px solid var(--accent-primary)!important;
}

.stProgress>div>div>div {
  background:linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))!important;
  border-radius:4px!important;
}

.streamlit-expanderHeader {
  background:var(--bg-secondary)!important;
  border:1px solid var(--border-light)!important;
  border-radius:8px!important;
  font-family:'Inter',sans-serif!important;
}

.stRadio>div {
  gap:0.8rem;
  flex-direction:column;
}

.stRadio>div>label {
  background:var(--bg-secondary)!important;
  border:1px solid var(--border-light)!important;
  border-radius:8px!important;
  padding:0.9rem 1.2rem!important;
  cursor:pointer!important;
  transition:all 0.2s ease!important;
  width:100%!important;
  font-family:'Inter',sans-serif!important;
  color:var(--text-primary)!important;
}

.stRadio>div>label:hover {
  border-color:var(--accent-primary)!important;
  background:rgba(52, 152, 219, 0.05)!important;
}

.stSlider [data-baseweb="slider"]>div {
  background:linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))!important;
}

code {
  font-family:'Inter',monospace!important;
  background:var(--bg-tertiary)!important;
  color:var(--accent-secondary)!important;
  padding:0.2em 0.5em!important;
  border-radius:4px!important;
  font-size:0.85em!important;
  border:1px solid var(--border-light)!important;
}

::-webkit-scrollbar {
  width:8px;
  height:8px;
}

::-webkit-scrollbar-track {
  background:var(--bg-main);
}

::-webkit-scrollbar-thumb {
  background:var(--border-dark);
  border-radius:4px;
}

::-webkit-scrollbar-thumb:hover {
  background:var(--text-secondary);
}

.genius-card {
  background:var(--bg-secondary);
  border:1px solid var(--border-light);
  border-radius:12px;
  padding:1.5rem;
  transition:all 0.2s ease;
}

.genius-card:hover {
  border-color:var(--accent-primary);
  box-shadow:0 4px 12px rgba(52, 152, 219, 0.1);
}

.genius-card-accent {
  background:rgba(52, 152, 219, 0.05);
  border-left:4px solid var(--accent-primary);
}

.feature-card {
  background:var(--bg-secondary);
  border:1px solid var(--border-light);
  border-radius:12px;
  padding:1.2rem;
  transition:all 0.2s ease;
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  cursor:pointer;
}

.feature-card:hover {
  border-color:var(--accent-primary);
  box-shadow:0 4px 12px rgba(52, 152, 219, 0.1);
  transform:translateY(-2px);
}

.badge {
  display:inline-block;
  padding:0.4rem 0.8rem;
  border-radius:6px;
  font-size:0.7rem;
  font-weight:600;
  font-family:'Inter',sans-serif;
  letter-spacing:0.05em;
  text-transform:uppercase;
  background:rgba(52, 152, 219, 0.1);
  border:1px solid var(--accent-primary);
  color:var(--accent-primary);
}

.sidebar-nav-section {
  color:var(--sidebar-text);
  padding:1rem 1.2rem;
  margin:0.5rem 0;
}

.sidebar-nav-title {
  font-family:'Inter',sans-serif;
  font-size:0.7rem;
  font-weight:700;
  letter-spacing:0.08em;
  text-transform:uppercase;
  color:rgba(236, 240, 241, 0.6);
  margin-bottom:0.8rem;
}

.sidebar-nav-button {
  padding:0.75rem 1rem;
  margin-bottom:0.6rem;
  border-radius:8px;
  background:rgba(255,255,255,0.1);
  border:1px solid rgba(255,255,255,0.15);
  transition:all 0.2s ease;
  color:var(--sidebar-text);
  cursor:pointer;
  font-size:0.9rem;
  font-weight:500;
  text-align:left;
  font-family:'Inter',sans-serif;
}

.sidebar-nav-button:hover {
  background:rgba(52, 152, 219, 0.25);
  border-color:rgba(52, 152, 219, 0.5);
  color:#ffffff;
}

.sidebar-nav-button.active {
  background:var(--accent-primary);
  border-color:var(--accent-primary);
  color:white;
}

.sidebar-feature-item {
  padding:0.9rem;
  margin-bottom:0.6rem;
  border-radius:8px;
  background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.1);
  transition:all 0.2s ease;
  color:var(--sidebar-text);
  cursor:pointer;
}

.sidebar-feature-item:hover {
  background:rgba(52, 152, 219, 0.2);
  border-color:rgba(52, 152, 219, 0.5);
}

.sidebar-feature-icon {
  font-size:1.3rem;
  margin-bottom:0.3rem;
}

.sidebar-feature-title {
  font-weight:600;
  font-size:0.8rem;
  margin-bottom:0.2rem;
  color:#ffffff;
}

.sidebar-feature-desc {
  font-size:0.65rem;
  color:rgba(236, 240, 241, 0.7);
  line-height:1.3;
}

#MainMenu {
  visibility:hidden;
}

footer {
  visibility:hidden;
}

header {
  visibility:hidden;
}

hr {
  border-color:var(--border-light)!important;
  margin:1.5rem 0!important;
  opacity:0.5;
}

.stAlert {
  border-radius:8px!important;
  border:1px solid var(--border-light)!important;
  background:var(--bg-secondary)!important;
}

.stMarkdown {
  color:var(--text-primary);
}

.stMarkdown a {
  color:var(--accent-primary);
  text-decoration:none;
  font-weight:500;
}

.stMarkdown a:hover {
  text-decoration:underline;
}

.section-title {
  font-family:'Inter',sans-serif;
  font-size:1.8rem;
  font-weight:700;
  margin-bottom:0.3rem;
  color:var(--text-primary);
}

.section-sub {
  font-size:0.95rem;
  color:var(--text-secondary);
  margin-bottom:1.5rem;
  font-family:'Inter',sans-serif;
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
        "current_page": "Dashboard",
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
        # Logo/Title
        st.markdown("""
        <div style="padding:1.2rem;text-align:center;border-bottom:1px solid rgba(255,255,255,0.15);margin-bottom:1rem;">
          <div style="font-family:'Inter',sans-serif;font-size:1.3rem;font-weight:700;
                      color:#ffffff;margin-bottom:0.2rem;">
            📚 SAT Prep
          </div>
          <div style="font-size:.65rem;color:rgba(236, 240, 241, 0.7);
                      letter-spacing:.08em;text-transform:uppercase;">
            Master Your Test
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Connection Status
        if st.session_state.groq_api_key:
            st.markdown("""
            <div style="background:rgba(39,174,96,.15);border:1px solid rgba(39,174,96,.3);
                        border-radius:6px;padding:6px 10px;font-size:.65rem;color:#27ae60;
                        margin:0 0.8rem 1rem;text-align:center;font-family:'Inter',sans-serif;font-weight:600;">
              ✓ API Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(231,76,60,.15);border:1px solid rgba(231,76,60,.3);
                        border-radius:6px;padding:6px 10px;font-size:.65rem;color:#e74c3c;
                        margin:0 0.8rem 1rem;text-align:center;font-family:'Inter',sans-serif;font-weight:600;">
              ⚠ API Not Connected
            </div>
            """, unsafe_allow_html=True)

        # User Stats
        if st.session_state.onboarded:
            total = st.session_state.math_score + st.session_state.rw_score
            acc = (st.session_state.correct_answers / st.session_state.total_questions * 100
                   if st.session_state.total_questions > 0 else 0)
            st.markdown(f"""
            <div style="background:rgba(52,152,219,0.12);border:1px solid rgba(52,152,219,0.2);
                        border-radius:10px;padding:0.9rem;margin:0 0.8rem 1.5rem;color:#ffffff;">
              <div style="font-family:'Inter',sans-serif;font-weight:600;font-size:.8rem;
                          margin-bottom:.6rem;color:#ffffff;">
                👤 {st.session_state.user_name}
              </div>
              <div style="display:flex;justify-content:space-between;font-size:.7rem;color:rgba(236,240,241,0.9);margin-bottom:4px;">
                <span>Score</span><span style="color:#5fc5f5;font-weight:600;">{total}</span>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:.7rem;color:rgba(236,240,241,0.9);margin-bottom:4px;">
                <span>Accuracy</span><span style="color:#5fc5f5;font-weight:600;">{acc:.0f}%</span>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:.7rem;color:rgba(236,240,241,0.9);">
                <span>⚡ XP</span><span style="color:#5fc5f5;font-weight:600;">{st.session_state.xp_points}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Main Navigation
        st.markdown(
            '<div class="sidebar-nav-section"><div class="sidebar-nav-title">Navigation</div></div>',
            unsafe_allow_html=True
        )

        current_page = st.session_state.current_page
        for i, page in enumerate(PAGES):
            is_active = page == current_page
            btn_class = "sidebar-nav-button active" if is_active else "sidebar-nav-button"
            
            if st.button(f"{page}", use_container_width=True, key=f"nav_{i}_{page}"):
                go_to_page(page)

        # Features Section
        st.markdown(
            '<div class="sidebar-nav-section" style="margin-top:1.5rem;"><div class="sidebar-nav-title">Features</div></div>',
            unsafe_allow_html=True
        )

        features = [
            ("AI Tutor", "Conversational learning"),
            ("Adaptive Practice", "Adjusts to your level"),
            ("Smart RAG", "Official SAT content"),
            ("Analytics", "Track progress"),
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div class="sidebar-feature-item">
              <div class="sidebar-feature-icon">{icon}</div>
              <div class="sidebar-feature-title">{title}</div>
              <div class="sidebar-feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        # Footer Stats
        st.markdown(
            '<div style="padding:1rem 0 0;border-top:1px solid rgba(255,255,255,0.1);margin-top:1.5rem;'
            'text-align:center;font-size:.65rem;color:rgba(236,240,241,0.5);">'
            f'Day {st.session_state.streak_days} · {st.session_state.total_questions} solved'
            '</div>',
            unsafe_allow_html=True
        )


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
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
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
    if not st.session_state.onboarded:
        render_onboarding()
    else:
        render_sidebar()
        route()


if __name__ == "__main__":
    main()
