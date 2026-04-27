"""ai_tutor.py — chat-based tutor"""
import streamlit as st
from helpers import section_header, get_accuracy
from ai_engine import chat_with_tutor


def render():
    section_header("Tutor",
                   "Conversational help, grounded in the digital SAT syllabus.")

    suggestions = [
        "Explain the quadratic formula with an example",
        "How do I tackle reading comprehension faster?",
        "When do I use a semicolon vs a colon?",
        "What's the difference between mean, median, mode?",
        "Give me a strategy for systems of equations",
        "Help me understand exponential functions",
    ]

    if not st.session_state.chat_history:
        st.markdown('<div class="panel-accent">', unsafe_allow_html=True)
        st.markdown(f"**Hi, {st.session_state.user_name or 'there'}.**")
        weak = ", ".join(f"`{w}`" for w in st.session_state.weak_topics) or "_still mapping your weak areas_"
        st.markdown(
            f"Ask about any digital SAT concept, problem, or strategy. "
            f"I'll keep your weak topics ({weak}) in mind.\n\n"
            f"**Try one of these to start:**"
        )
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(s, key=f"sg_{i}", use_container_width=True):
                    _send_message(s)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Render chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ── Chat input ──
    user_input = st.chat_input("Ask a question…")
    if user_input:
        _send_message(user_input)
        st.rerun()

    # ── Tools ──
    with st.expander("Tools"):
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Clear chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with c2:
            if st.button("Tip on weak topic", use_container_width=True):
                weak = st.session_state.weak_topics
                topic = weak[0] if weak else "SAT strategy"
                _send_message(f"Give me a quick teaching tip about {topic}.")
                st.rerun()
        with c3:
            if st.button("What should I study?", use_container_width=True):
                _send_message("Based on my profile, what's the single most impactful thing I should study right now?")
                st.rerun()

        st.caption(f"Messages: {len(st.session_state.chat_history)} · "
                   f"Memory window: last 10 turns.")


def _send_message(text: str):
    student = {
        "name": st.session_state.user_name,
        "math_score": st.session_state.math_score,
        "rw_score": st.session_state.rw_score,
        "target_score": st.session_state.target_score,
        "weak_topics": st.session_state.weak_topics,
        "total_questions": st.session_state.total_questions,
        "accuracy": get_accuracy(),
    }
    st.session_state.chat_history.append({"role": "user", "content": text})
    with st.spinner("Thinking…"):
        reply = chat_with_tutor(text, st.session_state.chat_history[:-1], student)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})