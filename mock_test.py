"""pages/mock_test.py — Timed full SAT module simulation"""
import random
import time
import streamlit as st
from helpers import section_header, badge_html, update_score_after_answer, get_accuracy
from ai_engine import QUESTION_BANK, explain_question


def render():
    section_header("🏆 Mock SAT Test",
                   "Full digital-SAT-style simulation with adaptive modules and AI review.")

    state = st.session_state.mock_test_state

    if state is None:
        _render_setup()
    elif state.get("phase") == "in_progress":
        _render_test()
    elif state.get("phase") == "results":
        _render_results()


def _render_setup():
    st.markdown('<div class="genius-card genius-card-accent">', unsafe_allow_html=True)
    st.markdown("### 📋 Test Format")
    st.markdown("""
The digital SAT has two sections:
- **Reading & Writing** — 54 questions, 64 minutes (2 modules of 27)
- **Math** — 44 questions, 70 minutes (2 modules of 22), calculator allowed

This mock test runs a **condensed simulation** with AI-curated questions across both sections, 
with a live timer, instant scoring, and an AI-generated review at the end.
""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        n_questions = st.selectbox("Length", ["Quick (10 q)", "Standard (20 q)", "Full (30 q)"], index=1)
    with c2:
        time_pressure = st.selectbox("Time mode", ["Relaxed", "Realistic", "Pressure"], index=1)
    with c3:
        sections = st.multiselect(
            "Sections",
            ["Math · Algebra", "Math · Advanced Math", "Math · Problem Solving & Data",
             "Math · Geometry & Trig", "Reading · Information & Ideas",
             "Reading · Craft & Structure", "Writing · Standard English",
             "Writing · Expression of Ideas"],
            default=["Math · Algebra", "Math · Advanced Math",
                     "Reading · Information & Ideas", "Writing · Standard English"],
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("🚀 Start Mock Test", type="primary", use_container_width=True):
        if not sections:
            st.error("Pick at least one section.")
            return
        n_map = {"Quick (10 q)": 10, "Standard (20 q)": 20, "Full (30 q)": 30}
        n = n_map[n_questions]
        time_map = {"Relaxed": 90, "Realistic": 60, "Pressure": 40}
        secs_per_q = time_map[time_pressure]

        # Build question set
        questions: list[dict] = []
        per_section = max(1, n // len(sections))
        for sec in sections:
            pool = QUESTION_BANK.get(sec, [])
            if pool:
                k = min(per_section, len(pool))
                picks = random.sample(pool, k)
                for p in picks:
                    p_copy = p.copy()
                    p_copy["topic"] = sec
                    questions.append(p_copy)
        # If short, top up
        all_pool = []
        for sec in sections:
            for q in QUESTION_BANK.get(sec, []):
                qc = q.copy()
                qc["topic"] = sec
                all_pool.append(qc)
        while len(questions) < n and all_pool:
            pick = random.choice(all_pool)
            if pick not in questions:
                questions.append(pick)
            else:
                # avoid infinite loop
                questions.append(pick.copy())
                break
        questions = questions[:n]
        random.shuffle(questions)

        st.session_state.mock_test_state = {
            "phase": "in_progress",
            "questions": questions,
            "answers": [None] * len(questions),
            "current": 0,
            "start_time": time.time(),
            "deadline": time.time() + secs_per_q * len(questions),
            "secs_per_q": secs_per_q,
        }
        st.rerun()


def _render_test():
    state = st.session_state.mock_test_state
    questions = state["questions"]
    idx = state["current"]
    q = questions[idx]
    total = len(questions)

    # Timer calculation
    remaining = max(0, int(state["deadline"] - time.time()))
    mins, secs = divmod(remaining, 60)
    
    # Auto-finish if time expires
    if remaining == 0:
        _finish_test()
        st.rerun()
        return
    
    answered_count = sum(1 for a in state["answers"] if a is not None)
    
    # Timer display with warning color when low
    timer_color = "#e74c3c" if remaining < 300 else "#3498db"  # Red if < 5 mins
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                background:var(--bg-secondary);border:2px solid {timer_color};
                border-radius:10px;padding:1rem 1.5rem;margin-bottom:1rem;">
      <div style="font-weight:600;color:var(--text-primary);">Question {idx+1} / {total}</div>
      <div style="text-align:center;">
        <div style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:0.3rem;">⏱️ Time Remaining</div>
        <div style="font-family:'Courier New',monospace;font-size:2rem;font-weight:700;
                    color:{timer_color};letter-spacing:0.15em;">{mins:02d}:{secs:02d}</div>
      </div>
      <div style="text-align:right;color:var(--text-secondary);">
        ✅ {answered_count} answered
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add auto-refresh JavaScript to update timer every second
    st.markdown("""
    <script>
    // Auto-refresh page every 2 seconds to keep timer running
    var refreshInterval = setInterval(function() {
        if (document.visibilityState === 'visible') {
            location.reload();
        }
    }, 2000);
    // Stop refreshing when page is hidden
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            clearInterval(refreshInterval);
        }
    });
    </script>
    """, unsafe_allow_html=True)

    st.progress((idx + 1) / total)

    # Question card
    st.markdown('<div class="genius-card">', unsafe_allow_html=True)
    st.markdown(badge_html(q.get("topic","SAT"), "blue") + " " +
                badge_html(q.get("difficulty","Medium"), "amber"),
                unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(f"#### {q['question']}")

    current_ans = state["answers"][idx]
    options = q["options"]
    default_idx = options.index(current_ans) if current_ans in options else 0
    choice = st.radio("Your answer:", options, index=default_idx if current_ans else 0,
                      key=f"mock_q_{idx}", label_visibility="collapsed")

    state["answers"][idx] = choice
    st.markdown('</div>', unsafe_allow_html=True)

    # Nav buttons
    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
            state["current"] = max(0, idx - 1)
            st.rerun()
    with c2:
        if st.button("➡️ Next", use_container_width=True, disabled=(idx >= total - 1)):
            state["current"] = min(total - 1, idx + 1)
            st.rerun()
    with c3:
        if st.button("📋 Question grid", use_container_width=True):
            st.session_state["show_q_grid"] = not st.session_state.get("show_q_grid", False)
            st.rerun()
    with c4:
        if st.button("🏁 Finish Test", type="primary", use_container_width=True):
            _finish_test()
            st.rerun()

    if st.session_state.get("show_q_grid"):
        st.markdown("---")
        st.markdown("**Question grid** — click any to jump.")
        grid_cols = st.columns(10)
        for i in range(total):
            done = state["answers"][i] is not None
            with grid_cols[i % 10]:
                label = f"{'✓' if done else ''}{i+1}"
                if st.button(label, key=f"jump_{i}", use_container_width=True):
                    state["current"] = i
                    st.session_state["show_q_grid"] = False
                    st.rerun()


def _finish_test():
    state = st.session_state.mock_test_state
    questions = state["questions"]
    answers = state["answers"]
    correct = sum(1 for q, a in zip(questions, answers) if a == q["correct"])
    total = len(questions)
    raw_pct = correct / total if total else 0

    # Approx scaled score (out of 1600)
    scaled = int(800 + raw_pct * 800)

    state["correct"] = correct
    state["total"] = total
    state["scaled"] = scaled
    state["phase"] = "results"
    state["finished_at"] = time.time()

    # Update progress
    for q, a in zip(questions, answers):
        if a is not None:
            update_score_after_answer(a == q["correct"], q.get("topic", ""), q.get("difficulty", "Medium"))

    if scaled >= st.session_state.target_score:
        st.balloons()


def _render_results():
    state = st.session_state.mock_test_state
    correct = state["correct"]
    total = state["total"]
    scaled = state["scaled"]
    pct = correct / total * 100 if total else 0

    # Time used
    elapsed = state.get("finished_at", time.time()) - state["start_time"]
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    section_header("🏁 Mock Test Complete!", f"Time used: {mins}m {secs}s")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score (estimated)", f"{scaled}/1600")
    c2.metric("Correct", f"{correct}/{total}")
    c3.metric("Accuracy", f"{pct:.0f}%")
    delta = scaled - (st.session_state.math_score + st.session_state.rw_score)
    c4.metric("vs current SAT", f"{delta:+d}")

    if scaled >= st.session_state.target_score:
        st.success(f"🎉 You hit your target score of {st.session_state.target_score}!")

    # Per-question review
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### 📋 Question Review")
    questions = state["questions"]
    answers = state["answers"]
    for i, (q, a) in enumerate(zip(questions, answers)):
        is_correct = a == q["correct"]
        emoji = "✅" if is_correct else ("⏭️" if a is None else "❌")
        with st.expander(f"{emoji} Q{i+1}: {q['question'][:80]}{'…' if len(q['question'])>80 else ''}"):
            st.markdown(f"**Topic:** {q.get('topic','')} · **Difficulty:** {q.get('difficulty','')}")
            st.markdown(f"**Your answer:** {a or '_(skipped)_'}")
            st.markdown(f"**Correct:** {q['correct']}")
            st.markdown(f"**Explanation:** {q.get('explanation','')}")
            if st.button("🤖 Get AI deep-dive", key=f"review_ai_{i}"):
                with st.spinner("AI tutor analyzing…"):
                    detail = explain_question(q, a or "(skipped)", is_correct)
                    st.markdown(detail)

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Take another test", use_container_width=True, type="primary"):
            st.session_state.mock_test_state = None
            st.rerun()
    with c2:
        if st.button("📊 Go to Analytics", use_container_width=True):
            st.session_state.mock_test_state = None
            st.session_state.current_page = "📊 Analytics"
            st.rerun()
