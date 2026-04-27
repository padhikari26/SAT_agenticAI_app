"""utils/helpers.py — gamification, scoring, helpers"""
import streamlit as st
from datetime import datetime


def update_score_after_answer(correct: bool, topic: str = "", difficulty: str = "Medium"):
    st.session_state.total_questions += 1
    if correct:
        st.session_state.correct_answers += 1
        delta = {"Easy": 5, "Medium": 10, "Hard": 20}.get(difficulty, 10)
        st.session_state.xp_points += delta
        is_math = "Math" in topic
        if is_math and st.session_state.math_score < 800:
            st.session_state.math_score = min(800, st.session_state.math_score + delta // 2)
        elif not is_math and st.session_state.rw_score < 800:
            st.session_state.rw_score = min(800, st.session_state.rw_score + delta // 2)
    st.session_state.practice_history.append({
        "topic": topic,
        "correct": correct,
        "difficulty": difficulty,
        "timestamp": datetime.now().isoformat(),
    })


def get_accuracy() -> float:
    if st.session_state.total_questions == 0:
        return 0.0
    return st.session_state.correct_answers / st.session_state.total_questions * 100


def get_badges() -> list[tuple[str, str, bool]]:
    """Returns list of (icon, name, earned) for the badge system."""
    q = st.session_state.total_questions
    acc = get_accuracy()
    xp = st.session_state.xp_points
    return [
        ("🌱", "First Steps",    q >= 1),
        ("🎯", "10 Questions",   q >= 10),
        ("⭐", "50 Questions",   q >= 50),
        ("🏆", "100 Questions",  q >= 100),
        ("🔥", "80% Accuracy",   acc >= 80 and q >= 10),
        ("💎", "90% Accuracy",   acc >= 90 and q >= 20),
        ("⚡", "500 XP",         xp >= 500),
        ("🚀", "1000 XP",        xp >= 1000),
        ("📚", "Concept Master", len(st.session_state.get("strong_topics", [])) >= 3),
        ("🧠", "Tutor Friend",   len(st.session_state.get("chat_history", [])) >= 5),
    ]


def predict_score() -> tuple[int, int]:
    """Predict total score and improvement potential."""
    current = st.session_state.math_score + st.session_state.rw_score
    acc = get_accuracy()
    q = st.session_state.total_questions
    if q < 5:
        potential = current
    else:
        bonus = int((acc - 50) * 4) if acc > 50 else 0
        potential = min(1600, current + bonus)
    return current, potential


def section_header(title: str, sub: str = ""):
    """Reusable section header."""
    st.markdown(
        f'<div class="section-title">{title}</div>'
        f'<div class="section-sub">{sub}</div>',
        unsafe_allow_html=True
    )


def badge_html(text: str, color: str = "blue") -> str:
    return f'<span class="badge b-{color}">{text}</span>'
