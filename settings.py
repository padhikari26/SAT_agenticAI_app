"""settings.py — user settings, profile, and data management"""
import json
import streamlit as st
from helpers import section_header


def render():
    section_header("Settings", "Manage your profile and data.")

    t1, t2, t3 = st.tabs(["Profile", "Data", "About"])

    with t1:
        st.markdown("**User Profile**")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "Name",
                value=st.session_state.user_name,
                help="Your display name"
            )
        with col2:
            target = st.number_input(
                "Target score",
                value=st.session_state.target_score,
                min_value=800,
                max_value=1600,
                step=10
            )

        if st.button("Save profile", type="primary", use_container_width=True):
            st.session_state.user_name = name
            st.session_state.target_score = target
            st.success("Profile saved.")

        st.markdown("---")

        st.markdown("**API Configuration**")
        if st.session_state.groq_api_key:
            st.markdown(
                '<div class="status-pill status-ok">● api connected</div>',
                unsafe_allow_html=True
            )
            st.caption("Loaded from environment (.env)")
        else:
            st.markdown(
                '<div class="status-pill status-err">● api not configured</div>',
                unsafe_allow_html=True
            )
            st.caption("Add GROQ_API_KEY to your .env file to enable generation features.")

    with t2:
        st.markdown("**Your Data**")
        st.markdown(f"""
- Questions solved: **{st.session_state.total_questions}**
- Correct answers: **{st.session_state.correct_answers}**
- XP earned: **{st.session_state.xp_points}**
- Chat messages: **{len(st.session_state.chat_history)}**
- Streak: **{st.session_state.streak_days}** days
        """)

        if st.button("Export progress (JSON)", use_container_width=True):
            data = {
                "name": st.session_state.user_name,
                "math_score": st.session_state.math_score,
                "rw_score": st.session_state.rw_score,
                "target_score": st.session_state.target_score,
                "total_questions": st.session_state.total_questions,
                "correct_answers": st.session_state.correct_answers,
                "xp_points": st.session_state.xp_points,
                "weak_topics": st.session_state.weak_topics,
                "strong_topics": st.session_state.strong_topics,
                "practice_history": st.session_state.practice_history,
                "study_plan": st.session_state.study_plan,
            }
            st.download_button(
                "Download progress.json",
                data=json.dumps(data, indent=2),
                file_name="sat_progress.json",
                mime="application/json",
            )

        st.markdown("---")
        st.markdown("**Reset**")
        if st.button("Reset progress", type="secondary", use_container_width=True):
            st.session_state["confirm_reset"] = True

        if st.session_state.get("confirm_reset"):
            st.warning("This will clear all stats, chats, and history.")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("Confirm reset", type="primary", use_container_width=True):
                    keep = {"groq_api_key", "user_name", "onboarded",
                            "current_page", "model_choice"}
                    for k in list(st.session_state.keys()):
                        if k not in keep:
                            del st.session_state[k]
                    st.success("Progress reset.")
                    st.rerun()
            with cc2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state["confirm_reset"] = False
                    st.rerun()

    with t3:
        st.markdown("**About**")
        st.markdown("""
A digital SAT preparation tool with adaptive practice, a concept library, flashcards,
mock tests, and progress analytics.

**Built with**
Python · Streamlit · Groq API · pandas

**Features**
- Personalized tutor with chat history
- Adaptive practice with real-time difficulty adjustment
- Concept library covering the official 2024+ syllabus
- Flashcard decks for any topic
- Timed mock tests with per-question review
- Performance analytics and a study planner
        """)