"""pages/dashboard.py — landing dashboard with progress, AI insight, quick actions"""
import streamlit as st
from helpers import section_header, get_accuracy, get_badges, predict_score, badge_html
from ai_engine import call_groq, TUTOR_SYSTEM


def render():
    user = st.session_state.user_name or "Student"
    section_header(f"👋 Welcome back, {user}",
                   "Your AI-powered SAT command center.")

    # ── Top metrics ──
    total, potential = predict_score()
    acc = get_accuracy()
    gap = max(0, st.session_state.target_score - total)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Score", f"{total}", f"{total - 800:+d} from baseline")
    c2.metric("Target", f"{st.session_state.target_score}", f"{gap} pts to go")
    c3.metric("Accuracy", f"{acc:.0f}%", f"{st.session_state.correct_answers}/{st.session_state.total_questions} correct")
    c4.metric("⚡ XP", f"{st.session_state.xp_points}", f"Day {st.session_state.streak_days} streak")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Two columns: AI insight + Quick actions ──
    left, right = st.columns([1.6, 1])

    with left:
        st.markdown('<div class="genius-card genius-card-accent">', unsafe_allow_html=True)
        st.markdown("### 🤖 Your Daily AI Insight")
        if "daily_insight" not in st.session_state:
            st.session_state.daily_insight = None
        if st.session_state.daily_insight is None:
            with st.spinner("AI tutor analyzing your progress…"):
                if st.session_state.total_questions > 0:
                    prompt = (
                        f"Give a 3-sentence motivational dashboard insight for {user}. "
                        f"Math: {st.session_state.math_score}/800, R&W: {st.session_state.rw_score}/800. "
                        f"Solved {st.session_state.total_questions} questions at {acc:.0f}% accuracy. "
                        f"Target: {st.session_state.target_score}. Weak: {', '.join(st.session_state.weak_topics) or 'still mapping'}. "
                        f"Be specific, warm, and end with one concrete next step in SAT Genius."
                    )
                else:
                    prompt = (
                        f"Welcome {user} to their first day on SAT Genius. "
                        f"Target: {st.session_state.target_score}. Focus areas: {', '.join(st.session_state.focus_areas)}. "
                        f"Give a warm, energizing 3-sentence intro and recommend they start with the Practice page."
                    )
                st.session_state.daily_insight = call_groq(
                    [{"role": "user", "content": prompt}], system=TUTOR_SYSTEM, max_tokens=220,
                )
        st.markdown(st.session_state.daily_insight)
        if st.button("🔄 Get a fresh insight", key="refresh_insight"):
            st.session_state.daily_insight = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Actions")
        if st.button("📝 Start Practice", use_container_width=True, key="qa_practice"):
            st.session_state.current_page = "📝 Practice"
            st.rerun()
        if st.button("🧠 Ask the AI Tutor", use_container_width=True, key="qa_tutor"):
            st.session_state.current_page = "🧠 AI Tutor"
            st.rerun()
        if st.button("🎴 Review Flashcards", use_container_width=True, key="qa_flash"):
            st.session_state.current_page = "🎴 Flashcards"
            st.rerun()
        if st.button("🏆 Take Mock Test", use_container_width=True, key="qa_mock"):
            st.session_state.current_page = "🏆 Mock Test"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Score breakdown ──
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### 📊 Score Breakdown")
    col_m, col_r = st.columns(2)
    with col_m:
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("**Math** " + badge_html(f"{st.session_state.math_score}/800", "blue"),
                    unsafe_allow_html=True)
        st.progress(st.session_state.math_score / 800)
        gap_m = max(0, (st.session_state.target_score // 2) - st.session_state.math_score)
        st.caption(f"Goal: {st.session_state.target_score // 2}  ·  {gap_m} pts to target")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("**Reading & Writing** " + badge_html(f"{st.session_state.rw_score}/800", "violet"),
                    unsafe_allow_html=True)
        st.progress(st.session_state.rw_score / 800)
        gap_r = max(0, (st.session_state.target_score // 2) - st.session_state.rw_score)
        st.caption(f"Goal: {st.session_state.target_score // 2}  ·  {gap_r} pts to target")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Badges ──
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### 🏅 Achievements")
    badges = get_badges()
    earned = sum(1 for _, _, e in badges if e)
    st.caption(f"{earned} / {len(badges)} unlocked")
    cols = st.columns(5)
    for i, (icon, name, got) in enumerate(badges):
        with cols[i % 5]:
            opacity = "1" if got else "0.25"
            ring = "rgba(245,158,11,.4)" if got else "var(--border)"
            st.markdown(f"""
            <div style="text-align:center;padding:.7rem;border:1px solid {ring};border-radius:12px;
                        opacity:{opacity};margin-bottom:.5rem;">
              <div style="font-size:1.6rem;">{icon}</div>
              <div style="font-size:.7rem;color:#94a3b8;font-family:'DM Mono',monospace;">{name}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Focus areas ──
    if st.session_state.focus_areas:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("### 🎯 Your Focus Areas")
        st.markdown(
            " ".join(badge_html(f, "blue") for f in st.session_state.focus_areas),
            unsafe_allow_html=True
        )

    if st.session_state.weak_topics:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("### ⚠️ Topics That Need Work")
        st.markdown(
            " ".join(badge_html(t, "rose") for t in st.session_state.weak_topics[:6]),
            unsafe_allow_html=True
        )
