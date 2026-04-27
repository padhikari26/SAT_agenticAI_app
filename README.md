# 🎯 SAT Genius — Agentic AI SAT Preparation Platform

> A comprehensive AI-powered SAT prep app built with Python, Streamlit, and Groq AI.  
> Featuring multi-agent orchestration, agentic RAG, adaptive learning, and generative AI.

---

## ✨ What makes this unique

While most SAT prep apps are static question banks with a chatbot bolted on, **SAT Genius** is a **fully agentic AI system** where every feature is powered by coordinated AI agents grounded in the official 2024+ digital SAT syllabus.

### 🤖 8 Specialized AI Agents
| Agent | Role |
|---|---|
| **Tutor Agent** | Multi-turn conversational teaching with memory |
| **Question-Gen Agent** | Creates original SAT-realistic questions on demand |
| **Explainer Agent** | Diagnoses wrong answers and teaches the underlying concept |
| **Concept-Teacher Agent** | Generates full lessons with examples, traps, mnemonics |
| **Analyst Agent** | Quantifies score-impact of weak areas |
| **Planner Agent** | Builds personalized week-by-week study roadmaps |
| **Flashcard Agent** | Generates spaced-repetition decks for any topic |
| **Hint Agent** | Gives nudge-style hints without revealing answers |

### 🧬 Agentic RAG
A curated knowledge base of every digital SAT (2024+) topic — formulas, common mistakes, weights, strategies. Keyword retrieval grounds every AI response in the official syllabus, eliminating hallucinations on test content.

### 📊 Adaptive Learning
Practice difficulty calibrates to your real-time accuracy. Weak topics surface automatically. The AI tutor knows your profile (scores, weak areas, history) on every turn.

### 🎨 Production-grade UI
- Custom dark-mode design with Syne + DM Sans typography
- Animated gradients, glow effects, badge system
- Responsive layout, multi-page navigation
- Gamified XP, streaks, achievements

---

## 🚀 Quick Start

### 1. Get your free Groq API key
Visit [console.groq.com](https://console.groq.com), sign up (free, no credit card), and create an API key. Free tier: ~30 requests/min, thousands per day.

### 2. Install dependencies
```bash
cd sat_genius
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Onboard with your name, paste your Groq key, and start practicing.

---

## 📁 Project Structure
```
sat_genius/
├── app.py                  # Streamlit entry, navigation, onboarding, global CSS
├── requirements.txt
├── README.md
├── app_pages/                  # One file per app section
│   ├── dashboard.py        # Progress overview + AI insight
│   ├── ai_tutor.py         # Agentic chat tutor
│   ├── practice.py         # Adaptive practice engine
│   ├── concepts.py         # Concept library with on-demand AI lessons
│   ├── flashcards.py       # AI-generated flashcards
│   ├── mock_test.py        # Timed full-SAT simulation
│   ├── analytics.py        # Charts + AI insights
│   ├── study_plan.py       # AI study planner
│   └── settings.py         # Config, profile, data export
└── utils/
    ├── ai_engine.py        # Groq client, 8 agents, RAG, knowledge base
    └── helpers.py          # Scoring, gamification, badges
```

---

## 🎓 For Your Scholarship Application

This project demonstrates:

### Software Engineering
- **Modular architecture**: each page is an independent module
- **Separation of concerns**: AI logic, UI, state, and helpers cleanly split
- **Robust error handling**: API key issues, rate limits, model fallbacks all handled gracefully
- **State management**: 20+ session state keys with defaults and persistence

### AI/ML Engineering
- **Multi-agent orchestration**: 8 specialized agents with role-specific system prompts
- **Agentic RAG**: knowledge-base retrieval injected into prompts at runtime
- **Adaptive algorithms**: difficulty calibration, weak-topic detection
- **Robust LLM I/O**: JSON extraction with fallback parsing, model fallbacks, offline degradation
- **Memory & context management**: conversation history with rolling window + student profile injection

### Product Design
- **Gamification**: XP, streaks, 10 achievement badges
- **Onboarding flow**: 60-second setup → personalized experience
- **9 connected features** (Dashboard, Tutor, Practice, Concepts, Flashcards, Mock Test, Analytics, Plan, Settings)
- **Educational best practices**: spaced repetition, immediate feedback, scaffolding

### Real-world Impact
- Solves a measurable problem (SAT prep is a $1B+ market)
- Free-tier deployable (Groq + Streamlit Cloud = $0)
- Aligned to the official College Board syllabus
- Demonstrably more sophisticated than commercial alternatives

---

## 🛠️ Tech Stack
- **Frontend/runtime**: Streamlit (Python)
- **AI inference**: Groq API (Llama 3.1, Llama 3.3, Gemma 2)
- **Data**: pandas for analytics
- **Custom CSS**: Syne (display) + DM Sans (body) + DM Mono (code)

---

## 🌐 Deployment

### Streamlit Cloud (free)
1. Push this folder to a GitHub repo
2. Visit [share.streamlit.io](https://share.streamlit.io), connect your repo
3. Set the main file as `app.py`
4. Done — your app is live at a public URL

### Local/Docker
```bash
docker run -p 8501:8501 -v $(pwd):/app -w /app python:3.11-slim \
  bash -c "pip install -r requirements.txt && streamlit run app.py"
```

---

## 📜 License
Built for educational and college application purposes. Modify and showcase freely.

---

**Built with ❤️ to demonstrate what one motivated student can build with modern AI tools.**
