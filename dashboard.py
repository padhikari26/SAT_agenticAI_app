"""dashboard.py — overview of progress and quick actions"""
import streamlit as st
from helpers import section_header, get_accuracy, get_badges, predict_score, badge_html


def render():
    user = st.session_state.user_name or "Student"

    st.title("Dashboard")
    st.caption(f"Overview for {user}")

    total, potential = predict_score()
    acc = get_accuracy()
    gap = max(0, st.session_state.target_score - total)

    # ── Metrics ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", total)
    c2.metric("Target", st.session_state.target_score)
    c3.metric("Accuracy", f"{acc:.0f}%")
    c4.metric("XP", st.session_state.xp_points)

    st.divider()

    # ── Status ──
    st.subheader("Status")

    if st.session_state.total_questions == 0:
        st.write(
            f"Start practicing to establish your baseline.\n\n"
            f"Target score: {st.session_state.target_score}"
        )
    else:
        st.write(
            f"Math: {st.session_state.math_score}/800\n\n"
            f"Reading & Writing: {st.session_state.rw_score}/800\n\n"
            f"Questions solved: {st.session_state.total_questions}\n\n"
            f"Accuracy: {acc:.0f}%"
        )

    st.divider()

    # ── Score Breakdown ──
    st.subheader("Score Breakdown")

    st.write("Math")
    st.progress(st.session_state.math_score / 800)

    st.write("Reading & Writing")
    st.progress(st.session_state.rw_score / 800)

    st.divider()

    # ── Actions ──
    st.subheader("Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Practice", use_container_width=True):
            st.session_state.current_page = "Practice"
            st.rerun()

        if st.button("Open Tutor", use_container_width=True):
            st.session_state.current_page = "Tutor"
            st.rerun()

    with col2:
        if st.button("Flashcards", use_container_width=True):
            st.session_state.current_page = "Flashcards"
            st.rerun()

        if st.button("Mock Test", use_container_width=True):
            st.session_state.current_page = "Mock Test"
            st.rerun()