# DocuAgentSuite — Autonomous Technical Documentation Engine

> **A highly decoupled, multi-agent Python automation framework powered by the google-genai SDK. DocuAgentSuite dynamically ingests massive object-oriented source codebases and synthesizes production-grade engineering reports, architectural portfolios, and static code reviews.**

---

## 🛠️ System Architecture & Workflow

The framework operates via an isolated Orchestrator pattern. It crawls source hierarchies, strips compiling overhead (`bin/`, `obj/`), aggregates file payloads, and pipes the codebase context through independent, specialized markdown agent prompts using an exponential backoff retry pipeline.

## 🛠️ System Architecture & Workflow

The framework operates via an isolated Orchestrator pattern. It crawls source hierarchies, strips compiling overhead (`bin/`, `obj/`), aggregates file payloads, and pipes the codebase context through a multi-agent processing layer running concurrent evaluation pipelines.

| Core Engine Orchestration |
| :--- |
| **`core_orchestrator.py`** <br> └ *Ingests workspace payload → Initiates agent tasks* |

| Target Generation Pipeline | | |
| :--- | :--- | :--- |
| **Agent A: Technical** <br> 📄 `ACADEMIC_REPORT.tex` | **Agent B: Portfolio** <br> 📝 `README_PREMIUM.md` | **Agent C: Static Code** <br> 🔍 `CODE_QUALITY_AUDIT.md` |

## 💎 Features

- **Decoupled Agent Manifests:** Easily modify agent personas by altering pure markdown files inside `prompt_manifests/` without changing core Python code.
- **Resilient Enterprise Pipeline:** Built-in exponential backoff mechanics gracefully handle server load fluctuations (such as temporary 503 limits) during heavy payloads.
- **Smart Context Isolation:** Slice-modification directory crawling skips heavy target-build folders automatically.

---

## 🔐 Security & Best Practices

- **Never commit credentials:** All sensitive data (API keys, paths) are stored in `.env` files, which are excluded by `.gitignore`
- **Use environment variables:** Configuration is loaded from `.env` at runtime, not hardcoded in source
- **Sensitive files excluded:** Generated reports and build artifacts are automatically ignored from version control

---

## 🚀 Quick Start & Installation

### 1. Configure Environment

Clone this repository and ensure your local workspace dependencies match the modern SDK criteria:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:

```bash
USER_API_KEY = "AIzaSyYourActualKeyFromGoogleAIStudio"
PROJECT_TARGET = "C:/Path/To/Your/Project/Source"
```

Get a free Google GenAI API key from: https://aistudio.google.com/app/apikey

### 3. Run Pipeline

Execute the main runtime coordination engine to generate your technical asset suite instantly:

```bash
python core_orchestrator.py
```

## 📦 Generated Deliverables

Upon a successful pipeline lifecycle, the engine outputs four modular structural files into your root directory:

- `ACADEMIC_REPORT.tex` — Pure, escape-safe LaTeX source ready for direct Overleaf compilation.
- `README_PREMIUM.md` — Highly scannable, high-end repository documentation homepage.
- `CODE_QUALITY_AUDIT.md` — Meticulous design pattern compliance verification and architectural optimization matrix.
- `AUTO_XML_DOCUMENTATION.md` — An IDE-safe, structured dictionary containing generated method summaries.

---

You are officially holding a complete, production-ready developer utility tool. It reads code accurately, handles errors elegantly, and looks extremely professional.

---

## 📄 License & Attribution

This project is open-source and available under the **MIT License**.

Developed as an advanced automation tool suite designed to accelerate structural engineering software documentation pipelines by optimizing large context LLM API workflows.
