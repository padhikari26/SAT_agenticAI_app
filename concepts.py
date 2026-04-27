"""pages/concepts.py — Comprehensive concept library with RAG-grounded AI lessons"""
import streamlit as st
from helpers import section_header, badge_html
from ai_engine import SAT_KNOWLEDGE_BASE, teach_concept


def render():
    section_header("📚 SAT Concept Library",
                   "Every digital SAT topic, explained on-demand by your AI tutor — grounded in the official syllabus.")

    # Group by section
    math_topics = {k: v for k, v in SAT_KNOWLEDGE_BASE.items() if v["section"] == "Math"}
    rw_topics = {k: v for k, v in SAT_KNOWLEDGE_BASE.items() if v["section"] == "Reading & Writing"}

    tab_math, tab_rw, tab_explore = st.tabs(["🧮 Math", "📖 Reading & Writing", "🔍 Free Explore"])

    with tab_math:
        _render_section(math_topics, "math")

    with tab_rw:
        _render_section(rw_topics, "rw")

    with tab_explore:
        st.markdown('<div class="genius-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Ask AI to teach any SAT topic")
        st.markdown("Type any concept — the AI tutor will create a full lesson for you.")
        custom = st.text_input("Topic", placeholder="e.g., 'completing the square', 'parallel structure'")
        depth = st.select_slider("Depth", ["Quick refresher", "Standard", "Deep dive"], value="Standard")
        if st.button("📖 Generate lesson", type="primary"):
            if custom.strip():
                with st.spinner("🤖 Building your lesson…"):
                    lesson = teach_concept(custom.strip(), depth)
                    st.session_state[f"lesson_custom"] = lesson
        if st.session_state.get("lesson_custom"):
            st.markdown("---")
            st.markdown(st.session_state["lesson_custom"])
        st.markdown('</div>', unsafe_allow_html=True)


def _render_section(topics: dict, prefix: str):
    if not topics:
        st.info("No topics in this section.")
        return
    for key, info in topics.items():
        with st.expander(f"**{info['title']}** · {info['weight']}", expanded=False):
            # Subtopic chips
            chips = " ".join(badge_html(t, "blue") for t in info["topics"][:6])
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)

            # Quick reference
            st.markdown("**📐 Core formulas / rules**")
            st.code(info["core"], language="text")

            st.markdown("**⚠️ Common mistakes**")
            for m in info["mistakes"]:
                st.markdown(f"- {m}")

            st.markdown("---")

            col1, col2 = st.columns([1, 1])
            cache_key = f"lesson_{prefix}_{key}"
            with col1:
                if st.button(f"🤖 Get AI deep-dive lesson",
                             key=f"learn_{key}",
                             use_container_width=True):
                    with st.spinner("AI tutor preparing the lesson…"):
                        st.session_state[cache_key] = teach_concept(info["title"], "Standard")
            with col2:
                if st.button(f"📝 Practice this topic",
                             key=f"prac_{key}",
                             use_container_width=True):
                    # Find matching practice topic
                    target = None
                    for t in [
                        "Math · Algebra", "Math · Advanced Math",
                        "Math · Problem Solving & Data", "Math · Geometry & Trig",
                        "Reading · Information & Ideas", "Reading · Craft & Structure",
                        "Writing · Standard English", "Writing · Expression of Ideas",
                    ]:
                        # Approximate match
                        if any(w.lower() in info["title"].lower() for w in t.split("·")[-1].strip().split()):
                            target = t
                            break
                    st.session_state.practice_topic = target or "Math · Algebra"
                    st.session_state.current_page = "📝 Practice"
                    st.rerun()

            if st.session_state.get(cache_key):
                st.markdown("---")
                st.markdown(st.session_state[cache_key])
