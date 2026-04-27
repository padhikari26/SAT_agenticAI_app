# SAT Prep

A digital SAT preparation app built with Streamlit and the Groq API.

## Overview

A modular study tool with adaptive practice, a concept library, flashcards, timed
mock tests, performance analytics, and a study planner. Question generation,
explanations, and conversational tutoring are powered by an LLM (Groq) with
retrieval grounded in the official 2024+ digital SAT syllabus.

## Features

- **Dashboard** — score, accuracy, streak, focus areas
- **Practice** — adaptive difficulty, generated or curated questions, explanations on demand
- **Tutor** — chat with conversational memory and student-profile injection
- **Concept Library** — every digital SAT topic with formulas, common mistakes, and lessons
- **Flashcards** — generated decks on any topic with flip + rate workflow
- **Mock Test** — timed simulation with per-question review
- **Analytics** — trends, accuracy by topic, history, written analysis
- **Study Plan** — week-by-week roadmap from current score to target
- **Settings** — profile, data export, reset

## Quick Start

### 1. Get a Groq API key

Sign up at [console.groq.com](https://console.groq.com) (free tier, no card required)
and create an API key.

### 2. Install dependencies

```bash
cd sat_prep
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

### 4. Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Project Structure

```
sat_prep/
├── app.py            # entry point, navigation, onboarding, global CSS
├── requirements.txt
├── README.md
├── dashboard.py      # progress overview
├── ai_tutor.py       # chat tutor
├── practice.py       # adaptive practice
├── concepts.py       # concept library
├── flashcards.py     # flashcards
├── mock_test.py      # mock exam
├── analytics.py      # analytics
├── study_plan.py     # study planner
├── settings.py       # settings
├── ai_engine.py      # Groq client, knowledge base, generation, RAG
└── helpers.py        # scoring, gamification, badges
```

## Architecture Notes

- **Page modules** — each top-level section is its own file with a `render()` function;
  `app.py` routes by `st.session_state.current_page`.
- **State** — all user state is stored in `st.session_state` with defaults set in
  `init_state()`. Reset preserves auth + onboarding flags.
- **Generation layer** — `ai_engine.py` wraps Groq calls behind small functions
  (`generate_question`, `explain_question`, `chat_with_tutor`, etc.). Every call has
  a JSON-extraction fallback and an offline-degradation path so the UI never breaks
  on a bad response.
- **Retrieval** — `SAT_KNOWLEDGE_BASE` is a static dict keyed by topic; relevant
  entries are injected into prompts at runtime to keep generated content on-syllabus.
- **Adaptive difficulty** — `Practice` reads recent accuracy off
  `st.session_state.practice_history` and bumps difficulty Easy → Medium → Hard.

## Tech Stack

- Streamlit (UI)
- Groq API (Llama 3.x)
- pandas (analytics)
- python-dotenv (config)

## Deployment

### Streamlit Cloud

1. Push to a GitHub repo.
2. At [share.streamlit.io](https://share.streamlit.io), connect the repo.
3. Set `app.py` as the main file.
4. Add `GROQ_API_KEY` as a secret in the app settings.

### Docker

```bash
docker run -p 8501:8501 -v $(pwd):/app -w /app python:3.11-slim \
  bash -c "pip install -r requirements.txt && streamlit run app.py"
```

## License

Modify and reuse freely.