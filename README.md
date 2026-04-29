# 🤖 [TalentLens] An AI Resume Screening System

An intelligent, multi-agent system that evaluates resumes against job descriptions using specialized AI agents that collaborate via a LangGraph workflow. It has been built with Django, REST API, TailwindCSS, and JavaScript.

[![Watch the video](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://drive.google.com/file/d/1pyE434wTlETYoYvfI9d3AZCW8xUjA6Hf/view?usp=sharing)

<video src="./TalentLens-demo.mp4" controls="controls" style="max-width: 100%;">
</video>

## 🎯 Overview

This system takes a resume (PDF, DOCX, or TXT) and a job description, then produces a structured recommendation about whether the candidate should proceed to an interview. Unlike simple keyword matching or single-prompt approaches, this system uses **multiple specialized agents** that each handle a specific aspect of the evaluation and pass structured data to each other.

### Key Features

- **Multi-Agent Architecture**: 6 specialized agents with clear responsibilities
- **LangGraph Orchestration**: Parallel execution where possible, with convergence for decision making
- **Structured Reasoning**: Every decision includes explainable reasoning
- **Human-in-the-Loop**: Automatic flagging of uncertain cases for human review
- **Error Handling**: Graceful degradation when parsing fails or data is incomplete

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │  Resume (PDF/   │
                    │  DOCX/TXT)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Document Parser │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────────┐     │     ┌────────▼────────┐
     │  Resume Parser  │     │     │  Job Analyzer   │
     │     Agent       │     │     │     Agent       │
     └────────┬────────┘     │     └────────┬────────┘
              │              │              │
     ┌────────▼────────┐     │              │
     │ Skill Extractor │     │              │
     │     Agent       │     │              │
     └────────┬────────┘     │              │
              │              │              │
              └──────────────┼──────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐           ┌────────▼────────┐
     │ Skills Matcher  │           │   Experience    │
     │     Agent       │           │   Evaluator     │
     └────────┬────────┘           └────────┬────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │    Decision     │
                    │   Synthesizer   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │      Output     │
                    │  with Reasoning │
                    └─────────────────┘
```

### Agents and Their Responsibilities

| Agent | Responsibility |
|-------|----------------|
| **Document Parser** | Extract text from PDF/DOCX/TXT files |
| **Resume Parser Agent** | Structure resume into sections (contact, education, experience) |
| **Skill Extractor Agent** | Identify and categorize skills (technical, soft, tools) |
| **Job Analyzer Agent** | Parse job requirements (required vs preferred) |
| **Skills Matcher Agent** | Compare skills with semantic matching |
| **Experience Evaluator Agent** | Assess experience relevance and gaps |
| **Decision Synthesizer Agent** | Combine all inputs into final recommendation |

## 📋 Prerequisites

- Python 3.10+
- An LLM API key (choose one):
  - **Gemini** (free): [Google AI Studio](https://makersuite.google.com/app/apikey)
  - **Groq** (free, faster): [console.groq.com](https://console.groq.com)

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/Anas436/TalentLens.git
cd "TalentLens"
```
### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Edit `.env` file and add your API key:

```bash
# Option 1: Use Gemini
GEMINI_API_KEY=your_gemini_key_here
LLM_PROVIDER=gemini

# Option 2: Use Groq (faster, recommended)
GROQ_API_KEY=your_groq_key_here
LLM_PROVIDER=groq
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

## 📤 Output Format

The system required output with the following fields:

```json
{
    "match_score": 0.76,
    "recommendation": "Proceed to technical interview",
    "requires_human": true,
    "confidence": 0.81,
    "reasoning_summary": "Strong backend skills with Python and Django. Limited exposure to large-scale system design. Recommend interview to assess scaling knowledge."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `match_score` | 0.0-1.0 | How well the candidate fits the role |
| `recommendation` | String | Suggested next step |
| `requires_human` | Boolean | Should a human review this decision? |
| `confidence` | 0.0-1.0 | System's confidence in the decision |
| `reasoning_summary` | String | Human-readable explanation |


## 🔧 Configuration

You can customize the system behavior via environment variables in `.env`:

```bash
# LLM Provider ("gemini" or "groq")
LLM_PROVIDER=groq

# Model settings
GEMINI_MODEL=gemini-2.0-flash      # or gemini-1.5-pro for better quality
GROQ_MODEL=llama-3.3-70b-versatile # Fast and capable
TEMPERATURE=0.3                    # Lower = more consistent

# Confidence thresholds
CONFIDENCE_THRESHOLD_LOW=0.6       # Below this triggers human review
MATCH_SCORE_AMBIGUOUS_LOW=0.4      # Ambiguous zone lower bound
MATCH_SCORE_AMBIGUOUS_HIGH=0.7     # Ambiguous zone upper bound
```

## 🧠 Why This is "Agentic"

This system demonstrates true agentic behavior:

### ✅ What Makes It Agentic

1. **Multiple Specialized Agents**: Each agent has one clear job (Single Responsibility)
2. **Structured Data Passing**: Agents communicate through Pydantic models, not raw text
3. **Decisions at Multiple Points**: Branching logic based on intermediate outputs
4. **Uncertainty Handling**: Low confidence → flag for human review
5. **State Evolution**: The `ScreeningState` accumulates knowledge through the pipeline

### ❌ What This Is NOT

- A single massive prompt that does everything
- Simple keyword matching
- A linear pipeline with no branching
- An unstructured text-in, text-out system

## 🔒 Human-in-the-Loop Design

The system automatically flags cases for human review when:

| Trigger | Why |
|---------|-----|
| Confidence < 60% | Agents unsure about their analysis |
| Score between 40-70% | Borderline candidates need judgment |
| Parsing errors | Resume couldn't be fully processed |
| Missing critical data | Key information unavailable |

## 🛡️ Error Handling

The system handles failures gracefully:

- **File not found**: Returns error with clear message
- **Unsupported format**: Suggests supported formats
- **API failure**: Flags for manual review instead of crashing
- **Malformed resume**: Extracts what's possible, notes issues
- **Empty job description**: Returns error, doesn't hallucinate

## 📁 Project Structure

```
TalentLens/
├── manage.py                # Django entry point
├── requirements.txt         # Dependencies
├── .env                     # Environment config
│
├── core/                  # Django app
│   ├── views.py           # API views
│   ├── forms.py           # Forms
│   └── urls.py            # URL routing
│
├── src/                 # Core AI system
│   ├── config.py        # Configuration management
│   ├── models.py        # Pydantic data models
│   ├── workflow.py      # LangGraph orchestration
│   ├── document_parser.py  # PDF/DOCX/TXT parsing
│   │
│   └── agents/
│       ├── base.py             # Base agent class
│       ├── resume_parser.py    # Resume Parser Agent
│       ├── skill_extractor.py  # Skill Extractor Agent
│       ├── job_analyzer.py     # Job Analyzer Agent
│       ├── skills_matcher.py   # Skills Matcher Agent
│       ├── experience_eval.py  # Experience Evaluator Agent
│       └── decision_synth.py   # Decision Synthesizer Agent
│
└── templates/              # HTML templates
```

## 🚧 What I'd Do With More Time

### High Priority

1. **Batch Processing**: Screen multiple resumes against one job description
2. **Caching Layer**: Cache parsed resumes to avoid re-processing
3. **Better PDF Parsing**: Use OCR for image-based PDFs (pytesseract)
4. **Structured Output Mode**: Use Gemini's structured output feature for more reliable JSON

### Medium Priority

5. **Resume Database**: Store processed resumes for future matching
6. **Custom Weights**: Allow recruiters to adjust skill vs. experience importance
7. **Interview Questions**: Generate role-specific questions based on gaps
8. **Bias Detection**: Flag potentially biased language in job descriptions

### Nice to Have

9. **Multi-Language Support**: Handle resumes in different languages
10. **ATS Integration**: Export to common Applicant Tracking Systems
11. **Web UI**: Simple Flask/FastAPI frontend for non-technical users
12. **Learning from Feedback**: Store human corrections to improve future matching
13. **Comparative Ranking**: Rank multiple candidates for same position

## 📄 License

MIT License - feel free to use and modify.

