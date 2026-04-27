"""practice.py — adaptive question practice"""
import random
import streamlit as st
from helpers import section_header, update_score_after_answer, get_accuracy, badge_html
from ai_engine import (
    generate_question, explain_question, get_hint,
    QUESTION_BANK, detect_weak_strong_topics,
)


TOPIC_LIST = list(QUESTION_BANK.keys())


def render():
    section_header("Practice",
                   "Difficulty calibrates to your performance. Each answer refines your profile.")

    # ── Topic & difficulty selector ──
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        topic = st.selectbox("Topic", ["Surprise me"] + TOPIC_LIST, key="practice_topic")
    with c2:
        difficulty = st.selectbox("Difficulty",
                                   ["Easy", "Medium", "Hard", "Adaptive"],
                                   index=3, key="practice_difficulty")
    with c3:
        source = st.selectbox("Source",
                              ["Generated", "Curated bank"],
                              key="practice_source")
    with c4:
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("New question", use_container_width=True):
            _new_question(topic, difficulty, source)
            st.rerun()

    if st.session_state.current_quiz is None:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Ready to practice?**")
        st.markdown(
            "Click **New question** to start. Difficulty will be picked based on your "
            "recent accuracy and weak areas if Adaptive is selected."
        )
        if st.button("Start", type="primary", use_container_width=True):
            _new_question(topic, difficulty, source)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    q = st.session_state.current_quiz

    # ── Question card ──
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    badges_html = (
        badge_html(q.get("topic", "SAT"), "blue") +
        badge_html(q.get("difficulty", "Medium"), "amber") +
        badge_html("generated" if q.get("_ai") else "curated",
                   "violet" if q.get("_ai") else "green")
    )
    st.markdown(badges_html, unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(f"#### {q['question']}")

    # Answer state
    answered_key = f"answered_{q.get('id', q['question'][:30])}"
    if answered_key not in st.session_state:
        st.session_state[answered_key] = False
    answered = st.session_state[answered_key]

    if not answered:
        choice = st.radio("Choose your answer:",
                          q["options"],
                          key=f"choice_{q.get('id','x')}",
                          label_visibility="collapsed")
        c_a, c_b, c_c = st.columns([1, 1, 4])
        with c_a:
            if st.button("Submit", type="primary", use_container_width=True):
                _submit_answer(q, choice)
                st.rerun()
        with c_b:
            if st.button("Hint", use_container_width=True):
                with st.spinner("Loading hint…"):
                    st.info(get_hint(q))
        with c_c:
            if st.button("Skip", use_container_width=True):
                _new_question(topic, difficulty, source)
                st.rerun()
    else:
        # Show result
        student_answer = st.session_state.get(f"submitted_{q.get('id','x')}", "")
        is_correct = student_answer == q["correct"]
        for opt in q["options"]:
            if opt == q["correct"]:
                st.markdown(
                    f'<div style="background:#f0fdf4;border:1px solid #bbf7d0;'
                    f'border-radius:6px;padding:0.6rem 0.9rem;margin:0.3rem 0;'
                    f'color:#15803d;font-family:var(--sans);">✓ {opt}</div>',
                    unsafe_allow_html=True
                )
            elif opt == student_answer and not is_correct:
                st.markdown(
                    f'<div style="background:#fef2f2;border:1px solid #fecaca;'
                    f'border-radius:6px;padding:0.6rem 0.9rem;margin:0.3rem 0;'
                    f'color:#b91c1c;font-family:var(--sans);">✗ {opt}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="background:var(--bg-alt);border:1px solid var(--border);'
                    f'border-radius:6px;padding:0.6rem 0.9rem;margin:0.3rem 0;'
                    f'color:var(--text-mute);font-family:var(--sans);">{opt}</div>',
                    unsafe_allow_html=True
                )

        # Quick explanation
        st.markdown("---")
        st.markdown(f"**Explanation:** {q.get('explanation', '')}")

        # Deep dive
        with st.expander("Detailed walkthrough", expanded=False):
            if st.button("Generate walkthrough", key=f"ai_exp_{q.get('id','x')}"):
                with st.spinner("Building walkthrough…"):
                    detail = explain_question(q, student_answer, is_correct)
                    st.session_state[f"ai_exp_{q.get('id','x')}"] = detail
            if st.session_state.get(f"ai_exp_{q.get('id','x')}"):
                st.markdown(st.session_state[f"ai_exp_{q.get('id','x')}"])

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Next question", type="primary", use_container_width=True):
                _new_question(topic, difficulty, source)
                st.rerun()
        with c2:
            if st.button("Discuss in tutor", use_container_width=True):
                msg = (
                    f"Help me understand this SAT question better:\n\n"
                    f"**Q:** {q['question']}\n\n"
                    f"I picked **{student_answer}** and the correct answer is **{q['correct']}**.\n\n"
                    f"Can you teach me the underlying concept?"
                )
                st.session_state.chat_history.append({"role": "user", "content": msg})
                st.session_state.current_page = "Tutor"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Session stats ──
    st.markdown("<br/>", unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    a.metric("Solved", st.session_state.total_questions)
    b.metric("Accuracy", f"{get_accuracy():.0f}%")
    c.metric("XP", st.session_state.xp_points)
    weak, strong = detect_weak_strong_topics(st.session_state.practice_history)
    st.session_state.weak_topics = weak
    st.session_state.strong_topics = strong
    d.metric("Weak topics", len(weak))


# ── helpers ─────────────────────────────────────────────────────────────
def _new_question(topic: str, difficulty: str, source: str):
    if topic == "Surprise me":
        topic = random.choice(TOPIC_LIST)
    if difficulty == "Adaptive":
        acc = get_accuracy()
        if acc < 50 or st.session_state.total_questions < 3:
            difficulty = "Easy"
        elif acc < 75:
            difficulty = "Medium"
        else:
            difficulty = "Hard"

    if source == "Generated":
        with st.spinner("Generating question…"):
            q = generate_question(topic, difficulty)
            q["_ai"] = True
    else:
        pool = QUESTION_BANK.get(topic, [])
        if not pool:
            pool = random.choice(list(QUESTION_BANK.values()))
        filtered = [x for x in pool if x.get("difficulty") == difficulty] or pool
        q = random.choice(filtered).copy()
        q["_ai"] = False

    q.setdefault("topic", topic)
    q.setdefault("difficulty", difficulty)
    q.setdefault("id", f"{topic}_{random.randint(1000, 9999)}")
    st.session_state.current_quiz = q
    answered_key = f"answered_{q['id']}"
    st.session_state[answered_key] = False


def _submit_answer(q: dict, choice: str):
    is_correct = (choice == q["correct"])
    update_score_after_answer(is_correct, q.get("topic", ""), q.get("difficulty", "Medium"))
    st.session_state[f"answered_{q.get('id','x')}"] = True
    st.session_state[f"submitted_{q.get('id','x')}"] = choice