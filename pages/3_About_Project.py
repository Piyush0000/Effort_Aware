"""
About Project Page — Research Objectives & AI Copilot System Documentation.
"""

import streamlit as st

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0B0F17; color: #F1F5F9; }
    
    .about-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-header">
    <h2 style="color:#FFF; margin:0;">ℹ️ About the Effort-Aware AI Tutor & Copilot</h2>
    <p style="color:#93C5FD; margin-top:0.3rem; margin-bottom:0;">Adaptive Scaffolding & Real-Time Copilot Platform in Programming Education</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
---
### 🎯 Primary Project Objectives

Standard Generative AI assistants often output complete copy-pasteable solutions on the first prompt, suppressing deeper student problem-solving and self-explanation. 

This research project builds an **Effort-Aware Generative AI Tutor** that calculates an **explainable observable effort proxy score ($E$)** from non-invasive interaction signals (code edit completeness, diff variance, reasoning text depth, and debugging notes) to deliver appropriately scaffolded assistance.

---
### 🤖 Key Platform Capabilities

1. **🎯 Curated Problem Bank Mode:**
   - 15+ built-in CS problems across 12 core topics (*Variables, Loops, Primes, Palindromes, Arrays, Strings, Searching, Sorting, Functions, Recursion, Time Complexity*).

2. **✏️ Custom Problem Builder:**
   - Bring your own custom programming problem! Define custom problem statements, constraints, example inputs/outputs, and starter code skeletons.

3. **🤖 AI Programming Copilot Assistant:**
   - Open-ended real-time Copilot chat drawer allowing students to ask syntax questions, debug code snippets, clarify algorithm logic, or request step-by-step guidance.

4. **⚡ Explainable Effort Proxy Scoring Engine:**
   - Computes $E \in [0, 100]$ via:
     $$E = 0.30 \cdot A + 0.25 \cdot C + 0.25 \cdot R + 0.20 \cdot T$$
   - **Level 1 — HINT (Score < 35.0):** High-level conceptual hints (full solutions withheld).
   - **Level 2 — GUIDED (35.0 ≤ Score < 70.0):** Algorithmic steps, pseudocode, and partial code skeletons.
   - **Level 3 — WORKED SOLUTION (Score ≥ 70.0):** Full reference code, line-by-line explanation, and time/space complexity.

---
### 🛡️ Safety & Privacy Commitments
1. **Safe Static Validation:** User code is evaluated using static pattern checks. Arbitrary `eval()` or `exec()` execution is avoided.
2. **Local Data Storage:** All attempt history is stored locally in SQLite (`tutor_data.db`) without transmitting personal data.
3. **Offline Fallback Engine:** Functions fully offline if no Gemini API Key is provided or network is disconnected.

---
### 📁 Research Documentation Files
- `docs/system_architecture.md`: System design, module dataflow, and Mermaid diagrams.
- `docs/methodology.md`: Research questions, mathematical formula rationale, and threats to validity.
- `docs/experiment_protocol.md`: Experimental protocol for A/B/C testing.
""")
