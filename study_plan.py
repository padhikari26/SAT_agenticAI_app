"""pages/study_plan.py — AI-generated personalized study plan"""
import streamlit as st
from helpers import section_header, get_accuracy, predict_score
from ai_engine import generate_study_plan


def render():
    section_header("🗺️ AI Study Plan",
                   "A personalized, week-by-week roadmap from current → target score.")

    # Inputs
    c1, c2, c3 = st.columns(3)
    with c1:
        weeks = st.number_input("Weeks until your test", min_value=1, max_value=24, value=8)
    with c2:
        daily_min = st.number_input("Daily study minutes", min_value=15, max_value=240, value=45, step=15)
    with c3:
        intensity = st.select_slider("Intensity",
                                      ["Light", "Moderate", "Intense"],
                                      value="Moderate")

    current_score = st.session_state.math_score + st.session_state.rw_score
    target = st.session_state.target_score
    gap = target - current_score

    st.markdown('<div class="genius-card">', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("Score gap", f"{gap} pts")
    b.metric("Total study time", f"{daily_min * 7 * weeks // 60} hrs")
    c.metric("Path", f"{current_score} → {target}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("🚀 Generate my AI study plan", type="primary", use_container_width=True):
        profile = {
            "name": st.session_state.user_name,
            "current_score": current_score,
            "target_score": target,
            "weak_areas": st.session_state.weak_topics,
            "strong_areas": st.session_state.strong_topics,
            "focus_areas": st.session_state.focus_areas,
            "daily_minutes": daily_min,
            "weeks": weeks,
            "intensity": intensity,
        }
        with st.spinner("🤖 AI strategist building your personalized plan…"):
            st.session_state.study_plan = generate_study_plan(profile)

    if st.session_state.study_plan:
        st.markdown('<div class="genius-card genius-card-accent">', unsafe_allow_html=True)
        st.markdown(st.session_state.study_plan)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📥 Download plan (.txt)", use_container_width=True):
                st.download_button(
                    "💾 Save Plan",
                    data=st.session_state.study_plan,
                    file_name=f"sat_study_plan_{st.session_state.user_name}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
        with c2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.study_plan = ""
                st.rerun()
        with c3:
            if st.button("📝 Start practicing", use_container_width=True, type="primary"):
                st.session_state.current_page = "📝 Practice"
                st.rerun()
    else:
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("### 💡 Tips for an effective plan")
        st.markdown("""
- **Be honest about time** — overestimating leads to plan abandonment within a week.
- **Take a Mock Test first** so the plan can target real weaknesses, not assumed ones.
- **Re-generate** monthly as your scores climb — the plan should evolve.
""")
        st.markdown('</div>', unsafe_allow_html=True)
