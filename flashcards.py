"""flashcards.py — flashcard decks"""
import streamlit as st
from helpers import section_header
from ai_engine import generate_flashcards


def render():
    section_header("Flashcards",
                   "Generate decks for any SAT topic. Flip, rate, and review.")

    # Topic & generation controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        topic = st.text_input("Topic for new deck",
                              placeholder="e.g., 'Quadratic functions', 'Comma rules'",
                              key="flash_topic")
    with c2:
        n = st.slider("Cards", 4, 12, 8)
    with c3:
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Generate deck", use_container_width=True, type="primary"):
            if topic.strip():
                with st.spinner("Building deck…"):
                    deck = generate_flashcards(topic.strip(), n)
                    st.session_state.flashcard_deck = deck
                    st.session_state.flashcard_index = 0
                    st.session_state.flashcard_flipped = False
            else:
                st.warning("Enter a topic above.")

    deck = st.session_state.flashcard_deck

    if not deck:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Or pick a preset deck**")
        presets = [
            "Algebra essentials",
            "Quadratic functions",
            "Geometry formulas",
            "Probability & Statistics",
            "Grammar rules — punctuation",
            "Reading strategy shortcuts",
            "Common SAT vocabulary",
            "Trigonometry basics",
        ]
        cols = st.columns(2)
        for i, p in enumerate(presets):
            with cols[i % 2]:
                if st.button(p, use_container_width=True, key=f"preset_{i}"):
                    with st.spinner(f"Building '{p}'…"):
                        st.session_state.flashcard_deck = generate_flashcards(p, 8)
                        st.session_state.flashcard_index = 0
                        st.session_state.flashcard_flipped = False
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ── Card viewer ──
    idx = st.session_state.flashcard_index
    total = len(deck)
    card = deck[idx]

    st.progress((idx + 1) / total)
    st.caption(f"Card {idx + 1} of {total}  ·  {card.get('difficulty', 'Medium')}")

    flipped = st.session_state.get("flashcard_flipped", False)

    border = "var(--accent)" if flipped else "var(--border-strong)"
    label = "QUESTION" if not flipped else "ANSWER"
    label_color = "var(--text-mute)" if not flipped else "var(--accent)"

    content = card.get("front", "") if not flipped else card.get("back", "")

    st.markdown(f"""
    <div style="background:var(--bg);border:1px solid {border};border-radius:8px;
                padding:2.5rem 1.5rem;min-height:240px;display:flex;flex-direction:column;
                justify-content:center;align-items:center;text-align:center;
                margin-bottom:1rem;">
      <div style="font-family:var(--mono);font-size:0.7rem;
                  letter-spacing:0.15em;color:{label_color};margin-bottom:1rem;">
        {label}
      </div>
      <div style="font-family:var(--sans);font-size:1.1rem;
                  line-height:1.55;color:var(--text);white-space:pre-wrap;max-width:600px;">
        {content}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if flipped and card.get("tip"):
        st.info(f"**Tip:** {card['tip']}")

    # ── Controls ──
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1.5, 1, 1])
    with c1:
        if st.button("← Prev", use_container_width=True, disabled=(idx == 0)):
            st.session_state.flashcard_index = max(0, idx - 1)
            st.session_state.flashcard_flipped = False
            st.rerun()
    with c2:
        if st.button("Flip", use_container_width=True, type="primary"):
            st.session_state.flashcard_flipped = not flipped
            st.rerun()
    with c3:
        if flipped:
            sub = st.columns(3)
            with sub[0]:
                if st.button("Hard", use_container_width=True, key="rate_hard"):
                    _next_card(deck, idx)
                    st.rerun()
            with sub[1]:
                if st.button("OK", use_container_width=True, key="rate_ok"):
                    _next_card(deck, idx)
                    st.rerun()
            with sub[2]:
                if st.button("Easy", use_container_width=True, key="rate_easy"):
                    st.session_state.xp_points += 5
                    _next_card(deck, idx)
                    st.rerun()
        else:
            st.caption("Flip to rate")
    with c4:
        if st.button("Next →", use_container_width=True, disabled=(idx >= total - 1)):
            _next_card(deck, idx)
            st.rerun()
    with c5:
        if st.button("New deck", use_container_width=True):
            st.session_state.flashcard_deck = []
            st.session_state.flashcard_index = 0
            st.rerun()


def _next_card(deck: list, idx: int):
    if idx < len(deck) - 1:
        st.session_state.flashcard_index = idx + 1
        st.session_state.flashcard_flipped = False
    else:
        st.session_state.xp_points += 25
        st.session_state.flashcard_index = 0
        st.session_state.flashcard_flipped = False