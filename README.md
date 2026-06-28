
# 30-Day AI App Challenge

Building one AI-powered Streamlit app every day for 30 days.  
Each app is a standalone tool that can be run independently.

---

## What this is

A daily coding challenge to go from beginner AI apps to production-ready multi-agent systems.  
Every app is built with Python and Streamlit, using free AI APIs (Groq, Gemini) for the first two weeks and more advanced setups (LangChain, LangGraph, RAG) for the later days.

---

## Progress

| Day | App | Status |
|-----|-----|--------|
| 01 | Chat with Memory (Groq) | ✅ Done |
| 02 | Prompt Lab | 🔲 |
| 03 | PDF Summarizer | 🔲 |
| 04 | Code Explainer | 🔲 |
| 05 | Email Writer | 🔲 |
| 06 | Text Analyzer | 🔲 |
| 07 | URL Summarizer | 🔲 |
| 08 | Doc Q&A Bot | 🔲 |
| 09 | Multi-PDF Chat | 🔲 |
| 10 | Resume–Job Matcher | 🔲 |
| 11 | Codebase Doc Writer | 🔲 |
| 12 | Meeting Processor | 🔲 |
| 13 | Research Paper Q&A | 🔲 |
| 14 | Text-to-SQL | 🔲 |
| 15 | GitHub PR Reviewer | 🔲 |
| 16 | Error Log Analyzer | 🔲 |
| 17 | Code Security Scanner | 🔲 |
| 18 | CSV Data Agent | 🔲 |
| 19 | Web Research Agent | 🔲 |
| 20 | API Test Generator | 🔲 |
| 21 | Git Commit Writer | 🔲 |
| 22 | Blog Writer Pipeline | 🔲 |
| 23 | Code Gen Pipeline | 🔲 |
| 24 | Job App Suite | 🔲 |
| 25 | Competitor Intel Agent | 🔲 |
| 26 | GitHub Issue Triager | 🔲 |
| 27 | Sprint Planner Agent | 🔲 |
| 28 | Full PR Agent | 🔲 |
| 29 | Auth + Persistence | 🔲 |
| 30 | Deploy + Analytics | 🔲 |

---

## Folder structure

```
30-day-ai-apps/
├── .streamlit/
│   └── secrets.toml        ← API keys (never committed)
├── apps/
│   ├── day01_chat_groq.py
│   ├── day02_prompt_lab.py
│   └── ...
├── shared/
│   ├── __init__.py
│   ├── claude_client.py
│   └── ui_helpers.py
├── data/                   ← test files (PDFs, CSVs)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Bhuvaneswari123457/30-day-ai-apps.git
cd 30-day-ai-apps
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API keys**

Create `.streamlit/secrets.toml` (this file is gitignored — never commit it):
```toml
GROQ_API_KEY    = "gsk_..."
GEMINI_API_KEY  = "AIza..."
```

Get free keys at:
- Groq → [console.groq.com](https://console.groq.com)
- Gemini → [aistudio.google.com](https://aistudio.google.com)

---

## Run any app

```bash
streamlit run apps/day01_chat_groq.py
streamlit run apps/day02_prompt_lab.py
```

Each app runs on `localhost:8501` and can be used independently.

---

## Tech stack

| Layer | Tools |
|-------|-------|
| Frontend | Streamlit |
| LLM APIs | Groq (Llama 3), Google Gemini, Anthropic Claude |
| AI frameworks | LangChain, LangGraph, CrewAI |
| Vector store | ChromaDB, FAISS |
| Backend | FastAPI, Python |
| Deployment | Streamlit Cloud |

---

## Why this project

This challenge is preparation for a **Forward Deployment Engineer** role in AI — a role that requires building working AI demos for customers quickly.  
The daily build practice trains the core FDE skill: taking a customer problem and shipping a working POC in under 2 hours.

---

## Author

**Bhuvaneswari Chodisetty**  
CS Graduate · NIT Rourkela · AI Engineer  
[GitHub](https://github.com/Bhuvaneswari123457)
