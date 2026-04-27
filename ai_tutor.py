"""pages/ai_tutor.py — Agentic chat tutor with RAG-grounded answers"""
import streamlit as st
from helpers import section_header, get_accuracy
from ai_engine import chat_with_tutor


def render():
    section_header("🧠 AI Tutor",
                   "Multi-turn agentic conversations grounded in the digital SAT syllabus.")

    # ── Quick prompt suggestions ──
    suggestions = [
        "Explain the quadratic formula with an example",
        "How do I tackle reading comprehension faster?",
        "When do I use a semicolon vs a colon?",
        "What's the difference between mean, median, mode?",
        "Give me a strategy for systems of equations",
        "Help me understand exponential functions",
    ]

    if not st.session_state.chat_history:
        st.markdown('<div class="genius-card genius-card-accent">', unsafe_allow_html=True)
        st.markdown("### 👋 Hi! I'm your AI tutor.")
        st.markdown(
            f"I know the **digital SAT** inside-out and I remember your weak areas: "
            f"{', '.join(st.session_state.weak_topics) or '(still learning about you)'}.\n\n"
            "Ask me to **explain a concept**, **walk through a problem**, "
            "or **strategize** for any section. Try one of these to start:"
        )
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(f"💬 {s}", key=f"sg_{i}", use_container_width=True):
                    _send_message(s)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Render chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])

    # ── Chat input ──
    user_input = st.chat_input("Ask about any SAT concept, problem, or strategy…")
    if user_input:
        _send_message(user_input)
        st.rerun()

    # ── Sidebar tools ──
    with st.expander("🛠️ Tutor Tools"):
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔄 Clear chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with c2:
            if st.button("💡 Get hint about my weak topic", use_container_width=True):
                weak = st.session_state.weak_topics
                topic = weak[0] if weak else "SAT strategy"
                _send_message(f"Give me a quick teaching tip about {topic}.")
                st.rerun()
        with c3:
            if st.button("🎯 Recommend what to study now", use_container_width=True):
                _send_message("Based on my profile, what's the single most impactful thing I should study right now?")
                st.rerun()

        st.caption(f"💬 Messages exchanged: {len(st.session_state.chat_history)} · "
                   f"AI agent has memory of the last 10 turns.")


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
    with st.spinner("🤖 Thinking…"):
        reply = chat_with_tutor(text, st.session_state.chat_history[:-1], student)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
