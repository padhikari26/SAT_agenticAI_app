"""
utils/ai_engine.py
══════════════════════════════════════════════════════════════════
Groq-powered AI engine with:
  • Agentic RAG over the digital SAT syllabus knowledge base
  • Multi-agent orchestration (Tutor, Question-Gen, Analyst, Planner)
  • Adaptive difficulty + memory-aware conversation
  • Robust fallbacks for offline mode
══════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import random
import re
import os
from typing import Any
from dotenv import load_dotenv

import streamlit as st

# Load environment variables from .env file
load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENTIC RAG — Digital SAT Knowledge Base (2024+ syllabus) ║
# ╚══════════════════════════════════════════════════════════════╝
SAT_KNOWLEDGE_BASE: dict[str, dict] = {
    "math_algebra": {
        "title": "Algebra (Heart of Algebra)",
        "section": "Math",
        "weight": "~35% of Math",
        "topics": [
            "Linear equations in one variable",
            "Linear equations in two variables",
            "Linear functions",
            "Systems of two linear equations",
            "Linear inequalities",
        ],
        "core": (
            "LINEAR EQUATIONS: ax+b=c → x=(c-b)/a\n"
            "SLOPE: m=(y₂-y₁)/(x₂-x₁); SLOPE-INTERCEPT: y=mx+b\n"
            "POINT-SLOPE: y-y₁=m(x-x₁)\n"
            "SYSTEMS: substitution, elimination, graphing\n"
            "INEQUALITIES: flip sign when ÷/× by negative\n"
            "ABSOLUTE VALUE: |ax+b|=c → ax+b=c OR ax+b=-c"
        ),
        "mistakes": [
            "Forgetting to flip inequality with negatives",
            "Confusing slope vs y-intercept",
            "Not verifying solutions in the original equation",
        ],
    },
    "math_advanced": {
        "title": "Advanced Math",
        "section": "Math",
        "weight": "~35% of Math",
        "topics": [
            "Equivalent expressions",
            "Nonlinear equations and systems",
            "Quadratic / polynomial / exponential functions",
            "Radicals and rational expressions",
            "Function notation and composition",
        ],
        "core": (
            "QUADRATIC FORMULA: x = (-b ± √(b²-4ac)) / 2a\n"
            "DISCRIMINANT b²-4ac: >0 two real, =0 one, <0 none\n"
            "VERTEX FORM: y=a(x-h)²+k → vertex (h,k)\n"
            "EXPONENTS: xᵐ·xⁿ=xᵐ⁺ⁿ; (xᵐ)ⁿ=xᵐⁿ; x⁻ⁿ=1/xⁿ\n"
            "EXPONENTIAL: y=a·bˣ (b>1 growth, 0<b<1 decay)\n"
            "FUNCTION COMPOSITION: (f∘g)(x)=f(g(x))"
        ),
        "mistakes": [
            "Sign errors in the quadratic formula",
            "Misidentifying vertex from standard form",
            "Forgetting domain restrictions on radicals",
        ],
    },
    "math_problem_solving": {
        "title": "Problem-Solving & Data Analysis",
        "section": "Math",
        "weight": "~15% of Math",
        "topics": [
            "Ratios, rates, proportions",
            "Percentages",
            "Units and unit conversions",
            "Tables, graphs, scatterplots",
            "Probability and statistics",
            "Sample stats & margin of error",
        ],
        "core": (
            "PERCENT: part/whole × 100\n"
            "% CHANGE: (new-old)/old × 100\n"
            "MEAN: Σ values / n\n"
            "MEDIAN: middle value sorted; MODE: most frequent\n"
            "PROBABILITY: favorable / total\n"
            "CONDITIONAL: P(A|B) = P(A∩B) / P(B)"
        ),
        "mistakes": [
            "Mixing mean / median / mode",
            "Forgetting unit conversions",
            "Misreading graph axes / scales",
        ],
    },
    "math_geometry": {
        "title": "Geometry & Trigonometry",
        "section": "Math",
        "weight": "~15% of Math",
        "topics": [
            "Area, perimeter, volume",
            "Lines, angles, triangles",
            "Right-triangle trig (SOHCAHTOA)",
            "Circles (arcs, sectors, equations)",
            "Complex numbers",
        ],
        "core": (
            "PYTHAGORAS: a²+b²=c²\n"
            "30-60-90: x : x√3 : 2x   |   45-45-90: x : x : x√2\n"
            "TRIG: sinθ=opp/hyp, cosθ=adj/hyp, tanθ=opp/adj\n"
            "CIRCLE: A=πr², C=2πr; Arc=(θ/360)·2πr\n"
            "VOLUME: prism lwh, cyl πr²h, cone (1/3)πr²h, sphere (4/3)πr³"
        ),
        "mistakes": [
            "Confusing sin/cos",
            "Using diameter where radius is needed",
            "Forgetting to convert degrees ↔ radians",
        ],
    },
    "rw_information": {
        "title": "Reading: Information & Ideas",
        "section": "Reading & Writing",
        "weight": "~26% of R&W",
        "topics": [
            "Central ideas and details",
            "Inferences",
            "Command of evidence (textual & quantitative)",
        ],
        "core": (
            "MAIN IDEA = central claim, not the topic\n"
            "EVIDENCE: pick the option *most directly* supporting/refuting the claim\n"
            "INFERENCE: a logical step *just beyond* the text — never far\n"
            "DATA QUESTIONS: read axis labels & legend FIRST"
        ),
        "mistakes": [
            "Picking answers that go beyond the passage",
            "Choosing too broad / too narrow main ideas",
            "Confusing details with the central claim",
        ],
    },
    "rw_craft": {
        "title": "Reading: Craft & Structure",
        "section": "Reading & Writing",
        "weight": "~28% of R&W",
        "topics": [
            "Words in context",
            "Text structure & purpose",
            "Cross-text connections",
        ],
        "core": (
            "WORDS-IN-CONTEXT: substitute the choice back in — only one fits tone & meaning\n"
            "PURPOSE: ask 'why did the author write this sentence here?'\n"
            "CROSS-TEXT: identify each author's stance, then compare"
        ),
        "mistakes": [
            "Picking the dictionary definition over context",
            "Confusing tone with topic",
            "Misreading one author's view as the other's",
        ],
    },
    "rw_expression": {
        "title": "Writing: Expression of Ideas",
        "section": "Reading & Writing",
        "weight": "~20% of R&W",
        "topics": [
            "Rhetorical synthesis",
            "Transitions",
        ],
        "core": (
            "TRANSITIONS: addition (also, moreover) | contrast (however, yet) | "
            "cause-effect (therefore, thus) | sequence (next, finally) | example (for instance)\n"
            "SYNTHESIS: read the goal first, THEN scan bullets for what fulfils it"
        ),
        "mistakes": [
            "Choosing a transition that doesn't match the logical relationship",
            "Picking 'pretty' answers that don't satisfy the stated goal",
        ],
    },
    "rw_conventions": {
        "title": "Writing: Standard English Conventions",
        "section": "Reading & Writing",
        "weight": "~26% of R&W",
        "topics": [
            "Sentence boundaries",
            "Subject-verb / pronoun-antecedent agreement",
            "Verb tense, voice, mood",
            "Punctuation (commas, semicolons, colons, dashes, apostrophes)",
            "Modifiers & parallelism",
        ],
        "core": (
            "SEMICOLON connects two INDEPENDENT clauses (= soft period)\n"
            "COLON introduces a list / explanation; left side must be complete\n"
            "COMMA + FANBOYS (For And Nor But Or Yet So) joins independent clauses\n"
            "ITS = possessive; IT'S = it is\n"
            "Each / every / either / neither = SINGULAR\n"
            "PARALLELISM: same grammatical form across a list"
        ),
        "mistakes": [
            "Comma splices",
            "Confusing its / it's, their / they're / there",
            "Mismatched verb tense in compound sentences",
        ],
    },
}


# ╔══════════════════════════════════════════════════════════════╗
# ║    Curated SAT-style question bank (offline fallback)        ║
# ╚══════════════════════════════════════════════════════════════╝
QUESTION_BANK: dict[str, list[dict]] = {
    "Math · Algebra": [
        {"id":"alg1","question":"If 3x + 7 = 22, what is the value of x?",
         "options":["3","5","7","29/3"],"correct":"5",
         "explanation":"Subtract 7: 3x = 15. Divide by 3: x = 5.",
         "difficulty":"Easy","topic":"Linear equations"},
        {"id":"alg2","question":"A line passes through (2, 3) and (6, 11). What is its slope?",
         "options":["1/2","2","4","8"],"correct":"2",
         "explanation":"m = (11−3)/(6−2) = 8/4 = 2.",
         "difficulty":"Easy","topic":"Linear functions"},
        {"id":"alg3","question":"Solve: 2x + y = 10 and x − y = 2.",
         "options":["x=2,y=6","x=4,y=2","x=6,y=-2","x=3,y=4"],"correct":"x=4,y=2",
         "explanation":"Add equations: 3x = 12 → x = 4. Then 4 − y = 2 → y = 2.",
         "difficulty":"Medium","topic":"Systems of equations"},
        {"id":"alg4","question":"If |2x − 6| = 10, which value of x is possible?",
         "options":["−2","2","8","Both A and C"],"correct":"Both A and C",
         "explanation":"2x−6=10 → x=8; 2x−6=−10 → x=−2. Both work.",
         "difficulty":"Medium","topic":"Absolute value"},
        {"id":"alg5","question":"4(x + 3) > 2x + 14. Solve for x.",
         "options":["x > 1","x < 1","x > −1","x < −1"],"correct":"x > 1",
         "explanation":"4x+12 > 2x+14 → 2x > 2 → x > 1.",
         "difficulty":"Medium","topic":"Linear inequalities"},
        {"id":"alg6","question":"f(x)=2x+5 is shifted down 3. What is the new y-intercept?",
         "options":["2","3","5","8"],"correct":"2",
         "explanation":"New: f(x)=2x+2. Y-intercept = 2.",
         "difficulty":"Easy","topic":"Linear transformations"},
    ],
    "Math · Advanced Math": [
        {"id":"adv1","question":"What are the roots of x² − 5x + 6 = 0?",
         "options":["x=1,6","x=2,3","x=−2,−3","x=−1,−6"],"correct":"x=2,3",
         "explanation":"Factor: (x−2)(x−3)=0 → x=2 or 3.",
         "difficulty":"Easy","topic":"Quadratics"},
        {"id":"adv2","question":"f(x) = x² − 4x + 7. Where is the vertex?",
         "options":["(2,3)","(4,7)","(−2,19)","(2,7)"],"correct":"(2,3)",
         "explanation":"x = −b/2a = 4/2 = 2; f(2) = 4−8+7 = 3.",
         "difficulty":"Medium","topic":"Quadratic functions"},
        {"id":"adv3","question":"If f(x)=3x²+2 and g(x)=x−1, find f(g(2)).",
         "options":["5","17","29","11"],"correct":"5",
         "explanation":"g(2)=1; f(1)=3(1)+2=5.",
         "difficulty":"Medium","topic":"Function composition"},
        {"id":"adv4","question":"Simplify (x² − 9)/(x − 3).",
         "options":["x + 3","x − 3","x² + 3","x + 9"],"correct":"x + 3",
         "explanation":"x²−9 = (x+3)(x−3); cancel (x−3): x+3.",
         "difficulty":"Medium","topic":"Rational expressions"},
        {"id":"adv5","question":"Population doubles every 5 years. From 1,000, how many in 15 years?",
         "options":["3,000","6,000","8,000","15,000"],"correct":"8,000",
         "explanation":"15/5 = 3 doublings: 1000·2³ = 8,000.",
         "difficulty":"Medium","topic":"Exponential growth"},
    ],
    "Math · Problem Solving & Data": [
        {"id":"ps1","question":"Item discounted from $80 to $60. Percent decrease?",
         "options":["20%","25%","33%","75%"],"correct":"25%",
         "explanation":"(80−60)/80·100 = 25%.","difficulty":"Easy","topic":"Percent change"},
        {"id":"ps2","question":"Mean of 5 numbers is 12. Four are 8,10,14,16. Find the fifth.",
         "options":["10","12","14","22"],"correct":"12",
         "explanation":"Sum = 60; known = 48; fifth = 12.",
         "difficulty":"Easy","topic":"Statistics"},
        {"id":"ps3","question":"Bag: 4 red, 3 blue, 2 green. P(not red)?",
         "options":["4/9","5/9","4/5","5/4"],"correct":"5/9",
         "explanation":"Not red = 5; total = 9; P = 5/9.",
         "difficulty":"Easy","topic":"Probability"},
        {"id":"ps4","question":"240 miles in 4 hours. At this rate, miles in 7 hours?",
         "options":["340","380","420","480"],"correct":"420",
         "explanation":"60 mph · 7 h = 420 mi.","difficulty":"Easy","topic":"Rates"},
    ],
    "Math · Geometry & Trig": [
        {"id":"geo1","question":"Right triangle, legs 6 and 8. Hypotenuse?",
         "options":["10","12","14","√28"],"correct":"10",
         "explanation":"6²+8²=100; √100=10. (3-4-5 ×2.)",
         "difficulty":"Easy","topic":"Pythagorean"},
        {"id":"geo2","question":"Circle, radius 5. Area?",
         "options":["10π","25π","50π","100π"],"correct":"25π",
         "explanation":"A = πr² = 25π.","difficulty":"Easy","topic":"Circles"},
        {"id":"geo3","question":"30-60-90 triangle, shortest leg 4. Hypotenuse?",
         "options":["4√2","4√3","8","12"],"correct":"8",
         "explanation":"Sides x : x√3 : 2x → 2·4 = 8.",
         "difficulty":"Medium","topic":"Special triangles"},
    ],
    "Reading · Information & Ideas": [
        {"id":"ri1","question":"An author argues climate action is urgent and cites five recent studies. The PRIMARY purpose of the citations is to:",
         "options":["entertain readers with science",
                    "provide evidence supporting the central claim",
                    "introduce alternative viewpoints",
                    "demonstrate the author's expertise"],
         "correct":"provide evidence supporting the central claim",
         "explanation":"In argumentative writing, evidence directly backs the claim — here, the call for urgent action.",
         "difficulty":"Easy","topic":"Author's purpose"},
        {"id":"ri2","question":"\"Despite initial resistance, renewables are now cost-competitive.\" The word DESPITE signals:",
         "options":["cause and effect","contrast/concession","sequence","example"],
         "correct":"contrast/concession",
         "explanation":"Despite acknowledges something (resistance) that might seem to contradict what follows.",
         "difficulty":"Easy","topic":"Text structure"},
    ],
    "Reading · Craft & Structure": [
        {"id":"rc1","question":"A character says \"Lovely weather!\" during a thunderstorm. This is:",
         "options":["metaphor","simile","verbal irony","foreshadowing"],
         "correct":"verbal irony",
         "explanation":"Saying the opposite of what is meant = verbal irony (sarcasm).",
         "difficulty":"Easy","topic":"Literary devices"},
    ],
    "Writing · Standard English": [
        {"id":"we1","question":"Choose: \"Each of the students ___ required to submit their essay.\"",
         "options":["are","is","were","have been"],"correct":"is",
         "explanation":"\"Each\" is singular, takes singular verb \"is.\"",
         "difficulty":"Medium","topic":"Subject-verb agreement"},
        {"id":"we2","question":"Which uses the semicolon correctly?",
         "options":["I love math; and science.",
                    "She studied hard; she passed the exam.",
                    "He ran; quickly to the store.",
                    "The book; was very long."],
         "correct":"She studied hard; she passed the exam.",
         "explanation":"Semicolons connect two INDEPENDENT clauses — both must be complete sentences.",
         "difficulty":"Medium","topic":"Punctuation"},
    ],
    "Writing · Expression of Ideas": [
        {"id":"ei1","question":"Best transition: \"She trained for months. ___, she won the championship.\"",
         "options":["However","Therefore","For instance","In contrast"],
         "correct":"Therefore",
         "explanation":"Cause-effect: training caused the win.",
         "difficulty":"Easy","topic":"Transitions"},
        {"id":"ei2","question":"Most concise version of: \"Due to the fact that it was raining, we cancelled.\"",
         "options":["Because it was raining, we cancelled.",
                    "Due to rain conditions, we made the decision to cancel.",
                    "We cancelled because of the rain that was falling.",
                    "The event was cancelled by us due to rain."],
         "correct":"Because it was raining, we cancelled.",
         "explanation":"\"Due to the fact that\" → \"Because.\" Active voice. Direct.",
         "difficulty":"Medium","topic":"Conciseness"},
    ],
}


# ╔══════════════════════════════════════════════════════════════╗
# ║    Groq Client                                              ║
# ╚══════════════════════════════════════════════════════════════╝
def get_groq_client() -> Any:
    if not GROQ_AVAILABLE:
        return None
    # Try to get API key from: session state (user input) → .env file → environment variable
    api_key = st.session_state.get("groq_api_key", "") or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


def call_groq(messages: list, system: str = "",
              model: str | None = None,
              temperature: float = 0.7,
              max_tokens: int = 1024) -> str:
    """Call Groq with retries and graceful fallback."""
    client = get_groq_client()
    if not client:
        return _offline_response(messages)

    chosen_model = model or st.session_state.get("model_choice", "llama-3.1-8b-instant")
    full_msgs = []
    if system:
        full_msgs.append({"role": "system", "content": system})
    full_msgs.extend(messages)

    fallback_models = [chosen_model, "llama-3.1-8b-instant", "llama3-8b-8192", "gemma2-9b-it"]
    last_err = None
    seen = set()
    for m in fallback_models:
        if m in seen:
            continue
        seen.add(m)
        try:
            resp = client.chat.completions.create(
                model=m, messages=full_msgs,
                temperature=temperature, max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception as e:
            last_err = str(e).lower()
            if "invalid_api_key" in last_err or "authentication" in last_err:
                return "🔑 Invalid Groq API key. Update it in **Settings**. Get a free key at console.groq.com."
            if "rate_limit" in last_err:
                return "⏱️ Groq rate-limit reached. Wait 30 seconds and try again."
            continue
    return f"⚠️ AI temporarily unavailable ({last_err[:80] if last_err else 'unknown'}). Using offline reasoning."


def _offline_response(messages: list) -> str:
    """Helpful offline message — never lies about being an AI."""
    last = messages[-1]["content"].lower() if messages else ""
    if any(w in last for w in ("explain", "what is", "how does", "why")):
        return ("📚 **Offline mode** — add your free Groq API key in Settings to unlock AI explanations. "
                "In the meantime, the **Concepts** page has expert-curated material on every SAT topic.")
    if "hint" in last:
        return "💡 **Hint**: Break the problem into smaller steps. List what you know and what you need."
    return "🔌 Connect Groq AI in Settings to get personalized responses (free at console.groq.com)."


# ╔══════════════════════════════════════════════════════════════╗
# ║    System Prompts (Multi-Agent Personalities)                ║
# ╚══════════════════════════════════════════════════════════════╝
TUTOR_SYSTEM = """You are SAT Genius, an expert tutor for the digital SAT (College Board, 2024+ format).

THE DIGITAL SAT FORMAT YOU TEACH:
• Reading & Writing: 54 questions, 64 minutes, 2 modules of 27 each (adaptive)
• Math: 44 questions, 70 minutes, 2 modules of 22 each (adaptive); calculator allowed throughout
• Score range 400–1600 (200–800 per section)

YOUR TEACHING STYLE:
• Break problems into clear, numbered steps
• Use real-world analogies for abstract concepts
• Highlight common traps and how to avoid them
• Use markdown: **bold** for key terms, `code` for formulas, bullet lists for steps
• Always end with a "Key Takeaway" line
• Be warm, encouraging, never condescending
• If a student is stuck, give a *hint* before the answer

You may be given context from a knowledge base — when present, ground your answer in it."""

QUESTIONGEN_SYSTEM = """You are an SAT question-writer. Generate ORIGINAL, exam-realistic SAT questions
that match the official digital SAT (2024+) style and difficulty calibration. Always output strict JSON."""

ANALYST_SYSTEM = """You are an SAT performance analyst. Analyze student data and produce specific,
actionable insights. Quantify score-impact estimates whenever possible. Use bullet structure and
concrete examples. Be honest but encouraging."""

PLANNER_SYSTEM = """You are an SAT study plan strategist. Create realistic, personalized weekly plans
tied to the student's score gap, weak areas, and time budget. Be specific about activities and
durations. Reference SAT Genius features (Practice, Concepts, Flashcards, Mock Test) by name."""


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 1: Conversational Tutor (with RAG)                  ║
# ╚══════════════════════════════════════════════════════════════╝
def chat_with_tutor(user_msg: str, history: list, student: dict) -> str:
    rag_context = rag_lookup(user_msg)
    sys = TUTOR_SYSTEM
    if rag_context:
        sys += f"\n\nRELEVANT KNOWLEDGE BASE CONTEXT:\n{rag_context}"
    sys += (
        f"\n\nSTUDENT PROFILE:\n"
        f"• Name: {student.get('name','Student')}\n"
        f"• Math: {student.get('math_score',400)}/800\n"
        f"• Reading & Writing: {student.get('rw_score',400)}/800\n"
        f"• Target: {student.get('target_score',1400)}\n"
        f"• Weak topics: {', '.join(student.get('weak_topics',[])) or 'none yet'}\n"
        f"• Questions solved: {student.get('total_questions',0)}\n"
        f"• Accuracy: {student.get('accuracy',0):.0f}%"
    )

    messages = []
    for m in history[-10:]:
        if m.get("role") in ("user", "assistant"):
            messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_msg})

    return call_groq(messages, system=sys, max_tokens=900)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 2: Question Explainer                               ║
# ╚══════════════════════════════════════════════════════════════╝
def explain_question(question: dict, student_answer: str, correct: bool) -> str:
    prompt = f"""A student {"correctly answered" if correct else "got wrong"} this SAT question.

QUESTION: {question.get('question','')}
OPTIONS: {' | '.join(question.get('options', []))}
STUDENT'S ANSWER: {student_answer}
CORRECT ANSWER: {question.get('correct','')}
TOPIC: {question.get('topic','SAT')}
DIFFICULTY: {question.get('difficulty','Medium')}

Provide a teaching explanation with these sections (use markdown headers):

### Why the correct answer works
[step-by-step]

### {"Why your answer was tempting (a common trap)" if not correct else "Other options ruled out"}
[address the wrong choices]

### Key concept
[the rule / formula / strategy this tests]

### Pro tip
[one specific tip for similar questions]

Keep it under 280 words."""
    return call_groq([{"role":"user","content":prompt}], system=TUTOR_SYSTEM, max_tokens=600)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 3: Concept Teacher                                  ║
# ╚══════════════════════════════════════════════════════════════╝
def teach_concept(topic: str, depth: str = "Standard") -> str:
    rag = rag_lookup(topic)
    extra = f"\n\nGROUND YOUR EXPLANATION IN THIS:\n{rag}" if rag else ""

    prompt = f"""Teach the SAT topic: **{topic}** at {depth} depth.{extra}

Use this structure (markdown):

## 🧭 Core Concept
[Clear, intuitive explanation a student can understand]

## 📐 Key Formulas / Rules
[Use code blocks for formulas; bullet for rules]

## 🧪 Worked Example
[Realistic SAT-style problem, fully solved step-by-step]

## ⚠️ Common Mistakes
[3 specific traps]

## 💡 Memory Trick
[One memorable mnemonic or shortcut]

## 🎯 SAT Strategy
[How this topic actually appears on the test]

Be engaging, visual, SAT-focused."""
    return call_groq([{"role":"user","content":prompt}], system=TUTOR_SYSTEM, max_tokens=1400)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 4: Question Generator                               ║
# ╚══════════════════════════════════════════════════════════════╝
def generate_question(topic: str, difficulty: str = "Medium") -> dict:
    prompt = f"""Generate ONE original SAT-style multiple-choice question.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY a JSON object — no prose, no markdown fences:
{{
  "question": "Full question text (use plain text, not LaTeX)",
  "options": ["A) opt1","B) opt2","C) opt3","D) opt4"],
  "correct": "B) opt2",
  "explanation": "Step-by-step solution with the key insight",
  "topic": "{topic}",
  "difficulty": "{difficulty}"
}}

REQUIREMENTS:
• All 4 options must be plausible distractors
• Only ONE correct answer
• Explanation must teach the concept, not just state the answer
• For math, use concrete numbers (not just variables)"""
    raw = call_groq([{"role":"user","content":prompt}],
                    system=QUESTIONGEN_SYSTEM, temperature=0.8, max_tokens=700)
    parsed = _safe_json_extract(raw)
    if parsed and "question" in parsed and "options" in parsed and "correct" in parsed:
        parsed.setdefault("topic", topic)
        parsed.setdefault("difficulty", difficulty)
        parsed.setdefault("explanation", "Solve carefully and verify your work.")
        return parsed
    # Fallback to bank
    pool = QUESTION_BANK.get(topic) or random.choice(list(QUESTION_BANK.values()))
    return random.choice(pool)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 5: Performance Analyst                              ║
# ╚══════════════════════════════════════════════════════════════╝
def analyze_performance(history: list, weak: list) -> str:
    if not history:
        return ("Once you complete a few practice questions, this page will show "
                "**AI-generated insights** — your strongest skills, what to fix first, "
                "and how many points each fix is likely to add.")
    recent = history[-25:]
    correct = sum(1 for h in recent if h.get("correct"))
    total = len(recent)
    by_topic: dict[str, dict] = {}
    for h in recent:
        t = h.get("topic", "Unknown")
        by_topic.setdefault(t, {"c": 0, "n": 0})
        by_topic[t]["n"] += 1
        if h.get("correct"):
            by_topic[t]["c"] += 1
    topic_lines = "\n".join(
        f"• {t}: {v['c']}/{v['n']} ({v['c']/v['n']*100:.0f}%)"
        for t, v in by_topic.items()
    )
    prompt = f"""Analyse this student's recent SAT performance.

Last {total} questions: {correct} correct ({correct/total*100:.0f}%)
Identified weak topics so far: {', '.join(weak) if weak else 'none'}

By topic:
{topic_lines}

Produce (markdown headers):
## 📊 Performance Summary
## 🏆 Strongest Skills
## ⚠️ Priority Improvement Areas
[Ranked, with rough score-impact estimates like "+15–25 pts"]
## 🎯 This Week's Action Plan
[3 specific, time-bound actions]
## 🚀 Motivational Insight
[1-2 sentences]

Be concrete with numbers, calibrated and honest."""
    return call_groq([{"role":"user","content":prompt}], system=ANALYST_SYSTEM, max_tokens=900)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 6: Study Plan Generator                             ║
# ╚══════════════════════════════════════════════════════════════╝
def generate_study_plan(profile: dict) -> str:
    prompt = f"""Create a personalised SAT study plan.

STUDENT:
• Name: {profile.get('name','Student')}
• Current score: {profile.get('current_score',1000)}
• Target score: {profile.get('target_score',1400)}
• Score gap: {profile.get('target_score',1400) - profile.get('current_score',1000)} pts
• Weak areas: {', '.join(profile.get('weak_areas',[])) or 'TBD from diagnostics'}
• Strong areas: {', '.join(profile.get('strong_areas',[])) or 'TBD'}
• Daily study minutes: {profile.get('daily_minutes',45)}
• Weeks until test: {profile.get('weeks',8)}
• Focus areas chosen: {', '.join(profile.get('focus_areas',[])) or 'all sections'}

Produce a structured plan with markdown headers:

## 📅 Phase 1 — Foundations (Weeks 1–{max(2, profile.get('weeks',8)//3)})
[Specific topics, daily breakdown, target activities]

## 🎯 Phase 2 — Targeted Practice (next third)
[Drilling weak areas, mixed sets, AI Tutor sessions]

## 🏁 Phase 3 — Test Mastery (final third)
[Timed sections, Mock Tests, refinement]

## 🗓️ Weekly Schedule Template
[Mon–Sun, specific activities, Genius features named]

## 📈 Score Trajectory
[Realistic per-phase score gains adding to the gap]

## 🛠 SAT Genius Features to Use
[Map each feature — AI Tutor, Practice, Concepts, Flashcards, Mock Test, Analytics — to specific moments in the plan]

Be specific, motivating, and realistic."""
    return call_groq([{"role":"user","content":prompt}], system=PLANNER_SYSTEM, max_tokens=1700)


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 7: Flashcard Generator                              ║
# ╚══════════════════════════════════════════════════════════════╝
def generate_flashcards(topic: str, n: int = 8) -> list[dict]:
    prompt = f"""Generate {n} SAT study flashcards for: {topic}.

Return ONLY a JSON array. Each card:
{{"front":"...","back":"...","tip":"...","difficulty":"Easy|Medium|Hard"}}

Cover: key formulas, rules, common mistakes, strategy shortcuts, vocabulary.
The 'back' should be brief (≤ 60 words). The 'tip' should be a memory trick."""
    raw = call_groq([{"role":"user","content":prompt}],
                    system=TUTOR_SYSTEM, temperature=0.7, max_tokens=1500)
    parsed = _safe_json_extract(raw)
    if isinstance(parsed, list) and parsed:
        return parsed[:n]
    return _fallback_cards()[:n]


def _fallback_cards() -> list[dict]:
    return [
        {"front":"Slope formula","back":"m = (y₂−y₁) / (x₂−x₁)\nRise over run.","tip":"Always subtract Y first, then X.","difficulty":"Easy"},
        {"front":"Quadratic formula","back":"x = (−b ± √(b²−4ac)) / 2a","tip":"\"Negative b, plus or minus...\"","difficulty":"Medium"},
        {"front":"Discriminant b²−4ac","back":">0 → 2 real | =0 → 1 real | <0 → none","tip":"Sign tells you root count.","difficulty":"Medium"},
        {"front":"Pythagorean Theorem","back":"a² + b² = c² (c = hypotenuse)","tip":"3-4-5, 5-12-13, 8-15-17 are common.","difficulty":"Easy"},
        {"front":"30-60-90 triangle","back":"x : x√3 : 2x (short : long : hypotenuse)","tip":"Shortest is opposite the smallest angle.","difficulty":"Medium"},
        {"front":"45-45-90 triangle","back":"x : x : x√2","tip":"Isoceles right — legs equal.","difficulty":"Easy"},
        {"front":"Percent change","back":"(new − old) / old × 100","tip":"Always divide by the ORIGINAL.","difficulty":"Easy"},
        {"front":"Mean vs median","back":"Mean = average; median = middle value when sorted.","tip":"Outliers move the mean, not the median.","difficulty":"Easy"},
        {"front":"Subject-verb agreement","back":"\"Each\", \"every\", \"either\", \"neither\" → singular verb.","tip":"Cover the prepositional phrase.","difficulty":"Medium"},
        {"front":"Semicolon rule","back":"Connects two independent clauses.","tip":"= a soft period; both sides complete.","difficulty":"Medium"},
        {"front":"Its vs it's","back":"its = possessive; it's = it is.","tip":"Replace with \"it is\" — fits? use \"it's.\"","difficulty":"Easy"},
        {"front":"Verbal irony","back":"Saying the opposite of what's meant.","tip":"Sarcasm = words ≠ meaning.","difficulty":"Easy"},
    ]


# ╔══════════════════════════════════════════════════════════════╗
# ║    AGENT 8: Hint Generator                                  ║
# ╚══════════════════════════════════════════════════════════════╝
def get_hint(question: dict) -> str:
    prompt = f"""Give ONE short hint (under 40 words) for this SAT question. Do NOT reveal the answer — guide the student to the next step.

Question: {question.get('question','')}
Topic: {question.get('topic','')}
"""
    return call_groq([{"role":"user","content":prompt}],
                     system=TUTOR_SYSTEM, temperature=0.6, max_tokens=120)


# ╔══════════════════════════════════════════════════════════════╗
# ║    Agentic RAG: keyword retrieval over knowledge base        ║
# ╚══════════════════════════════════════════════════════════════╝
def rag_lookup(query: str) -> str:
    """Lightweight keyword RAG over the SAT knowledge base."""
    q = query.lower()
    keyword_to_kb = {
        "algebra": "math_algebra", "linear": "math_algebra", "system": "math_algebra",
        "inequality": "math_algebra", "slope": "math_algebra",
        "quadratic": "math_advanced", "exponential": "math_advanced",
        "function": "math_advanced", "polynomial": "math_advanced", "rational": "math_advanced",
        "percent": "math_problem_solving", "probability": "math_problem_solving",
        "statistic": "math_problem_solving", "mean": "math_problem_solving",
        "median": "math_problem_solving", "ratio": "math_problem_solving", "rate": "math_problem_solving",
        "geometry": "math_geometry", "triangle": "math_geometry", "circle": "math_geometry",
        "pythagorean": "math_geometry", "trig": "math_geometry", "sine": "math_geometry",
        "main idea": "rw_information", "evidence": "rw_information",
        "infer": "rw_information", "passage": "rw_information",
        "tone": "rw_craft", "irony": "rw_craft", "metaphor": "rw_craft",
        "context": "rw_craft", "purpose": "rw_craft",
        "transition": "rw_expression", "concis": "rw_expression",
        "synthesis": "rw_expression",
        "comma": "rw_conventions", "semicolon": "rw_conventions",
        "colon": "rw_conventions", "verb": "rw_conventions",
        "pronoun": "rw_conventions", "tense": "rw_conventions",
        "grammar": "rw_conventions", "punctuation": "rw_conventions",
    }
    hits = []
    seen: set[str] = set()
    for kw, key in keyword_to_kb.items():
        if kw in q and key not in seen and key in SAT_KNOWLEDGE_BASE:
            kb = SAT_KNOWLEDGE_BASE[key]
            hits.append(
                f"[{kb['title']}] ({kb['weight']})\n{kb['core']}\n"
                f"Mistakes: {'; '.join(kb['mistakes'])}"
            )
            seen.add(key)
            if len(hits) >= 2:
                break
    return "\n\n".join(hits)


def detect_weak_strong_topics(history: list) -> tuple[list[str], list[str]]:
    if not history:
        return [], []
    by_topic: dict[str, dict] = {}
    for h in history:
        t = h.get("topic", "Unknown")
        by_topic.setdefault(t, {"c": 0, "n": 0})
        by_topic[t]["n"] += 1
        if h.get("correct"):
            by_topic[t]["c"] += 1
    weak, strong = [], []
    for t, v in by_topic.items():
        if v["n"] >= 2:
            acc = v["c"] / v["n"]
            if acc < 0.6:
                weak.append(t)
            elif acc >= 0.85:
                strong.append(t)
    return weak, strong


def _safe_json_extract(text: str):
    """Extract JSON from possibly-fenced text."""
    if not isinstance(text, str):
        return None
    cleaned = re.sub(r'```(?:json)?\s*', '', text)
    cleaned = cleaned.replace('```', '').strip()
    # Try array first
    arr = re.search(r'\[\s*\{.*\}\s*\]', cleaned, re.DOTALL)
    obj = re.search(r'\{.*\}', cleaned, re.DOTALL)
    for candidate in (arr, obj):
        if candidate:
            try:
                return json.loads(candidate.group())
            except Exception:
                continue
    return None


# Available Groq models (current as of 2024+)
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "gemma2-9b-it",
]
