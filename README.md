# 🎓 An Effort-Aware Generative AI Framework for Reducing Cognitive Offloading in Programming Education

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![AI Provider](https://img.shields.io/badge/Google--GenAI-Gemini%202.5-4285F4.svg)](https://ai.google.dev/)
[![Tests](https://img.shields.io/badge/Pytest-100%25%20Passed-brightgreen.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Framework Overview
**An Effort-Aware Generative AI Framework for Reducing Cognitive Offloading in Programming Education** is an intelligent, research-grade programming education platform designed to mitigate unreflective cognitive offloading by providing **progressively adaptive scaffolding** rather than immediately revealing full code solutions.

Standard Generative AI assistants often output complete copy-pasteable solutions on the first prompt, suppressing deeper student problem-solving and self-explanation. This framework addresses cognitive offloading by calculating an **explainable observable effort proxy score ($E$)** based on non-invasive interaction signals (code edit diffs, reasoning text depth, and testing notes) to deliver appropriately scaffolded assistance.

---

## 🔬 Core Framework Features & Architecture

1. **Explainable Effort Proxy Engine:**
   - Computes a bounded score $E \in [0, 100]$ using the deterministic formula:
     $$E = 0.30 \cdot A + 0.25 \cdot C + 0.25 \cdot R + 0.20 \cdot T$$
   - **$A$ (Attempt Completeness):** Code structure and non-comment syntax.
   - **$C$ (Code Modification Variance):** Edit diff variance relative to starter template.
   - **$R$ (Reasoning Depth):** Explanation length and CS domain keyword density.
   - **$T$ (Testing Engagement):** Test inputs tried, expected outputs, and debugging notes.

2. **Scaffolded Assistance Policy:**
   - **Level 1 — HINT (Score < 35.0):** Conceptual clues & next steps (full code solutions withheld).
   - **Level 2 — GUIDED (35.0 ≤ Score < 70.0):** Algorithmic steps, pseudocode, and partial code skeletons.
   - **Level 3 — WORKED SOLUTION (Score ≥ 70.0):** Complete reference implementation with line-by-line explanation and time/space complexity analysis.

3. **Dual AI Engine with Offline Fallback & Real-Time Copilot:**
   - Powered by official `google-genai` SDK for Google Gemini models.
   - Includes an **AI Programming Copilot** for open-ended coding questions.
   - Includes a **deterministic offline fallback provider** utilizing pre-authored scaffolds if API keys are absent or network requests fail.

4. **15+ Original Educational Problems + Custom Problem Builder:**
   - Covers core topics: *Variables, Conditionals, Loops, Primes, Palindromes, Arrays, Strings, Searching, Sorting, Functions, Recursion, Time Complexity*.
   - Allows users to build and evaluate custom programming problems dynamically.

5. **Publication-Grade Research Analytics:**
   - Built-in Plotly visualizations (Polar Radar plots, Violin Density plots, Grouped Confidence Bars, Mastery Curves) comparing 3 scaffolding policies (*Immediate Disclosure*, *Fixed Hints*, *Effort-Aware Scaffolding*).

---

## 📐 Project Structure

```
effort_aware_ai_tutor/
├── app.py                         # Main Streamlit Framework Application
├── config.py                      # System Constants, Weights & Level Thresholds
├── effort_engine.py               # Explainable Effort Proxy Scoring Engine
├── tutor_engine.py                # Gemini SDK & Offline Fallback Tutor Engine
├── question_bank.py               # Question Bank Loader & Filters
├── database.py                    # SQLite Storage & Parameterized SQL Queries
├── analytics.py                   # Advanced Plotly Research Visualizations
├── vercel.json                    # Vercel Deployment Configuration
├── requirements.txt               # Python Dependencies
├── .env.example                   # API Key Environment Example
├── .gitignore                     # Git Exclusion Rules
├── README.md                      # Comprehensive Framework Documentation
├── LICENSE                        # MIT License
├── pytest.ini                     # Pytest Configuration
├── pages/
│   ├── 1_Learning_Dashboard.py    # Student Progress Dashboard
│   ├── 2_Research_Analytics.py    # Experimental Scaffolding Analytics
│   └── 3_About_Project.py         # Research Objectives & Architecture Overview
├── data/
│   └── questions.json             # 15+ Original CS Programming Problems
├── tests/
│   ├── test_effort_engine.py      # Unit Tests for Scoring Logic
│   ├── test_tutor_engine.py       # Unit Tests for AI & Fallback Providers
│   ├── test_database.py           # Unit Tests for Database Operations
│   └── test_question_bank.py      # Unit Tests for Question Bank
├── scripts/
│   ├── seed_database.py           # Synthetic Benchmark Dataset Seeder
│   └── run_checks.py              # Automated System Verification Suite
├── outputs/
│   └── .gitkeep                   # Output Directory Artifact Tracking
└── docs/
    ├── system_architecture.md     # Architecture Diagram & System Specifications
    ├── methodology.md             # Research Questions & Formula Rationale
    └── experiment_protocol.md     # A/B/C Experimental Design Protocol
```

---

## 🚀 Installation & Local Execution (Windows)

### Prerequisites
- Python 3.10+ installed on Windows
- Git (optional, for version control)

### Step 1: Open Terminal & Navigate to Project
```powershell
cd C:\Users\Hansika Gupta\Desktop\project\effort_aware_ai_tutor
```

### Step 2: Activate Virtual Environment
```powershell
.venv\Scripts\activate
```

### Step 3: Run Automated System Verification & Tests
```powershell
python scripts\run_checks.py
```

### Step 4: Launch the Streamlit Application
```powershell
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`.

---

## 🌐 Cloud Deployment Instructions

### Deploying to GitHub & Vercel / Streamlit Cloud

1. **Push to GitHub:**
   ```powershell
   git remote add origin https://github.com/<YOUR_USERNAME>/effort_aware_ai_tutor.git
   git push -u origin main
   ```

2. **Streamlit Community Cloud (Recommended):**
   - Connect GitHub at [share.streamlit.io](https://share.streamlit.io) $\rightarrow$ Select repo $\rightarrow$ Main file: `app.py` $\rightarrow$ Deploy.

3. **Vercel Deployment:**
   - Import GitHub repository on [vercel.com](https://vercel.com) (Vercel automatically detects `vercel.json` and builds the Python app).

---

## ⚠️ Academic Methodological Disclaimer
> **Important Note:** The Effort Proxy Score ($E$) calculated by this software is an **observable behavioral engagement metric** derived strictly from user interface interaction data (code edits, text explanation length, testing notes). It does **NOT** claim to measure innate human intelligence, intrinsic cognitive capacity, or underlying motivation. Furthermore, experimental results shown in the analytics tab utilize reproducible synthetic benchmark data for protocol validation unless formal human-subject trial data is collected under appropriate institutional approval.

---

## 📄 License
This project is released under the [MIT License](LICENSE).
