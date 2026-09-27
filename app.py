"""
Effort-Aware Generative AI Framework for Reducing Cognitive Offloading in Programming Education.
"""

import streamlit as st
import os
import uuid
import dotenv
from question_bank import QuestionBank, Question
from effort_engine import EffortEngine
from tutor_engine import TutorEngine
from database import DatabaseManager
from config import APP_NAME, APP_SUBTITLE, APP_ICON, SUPPORTED_LANGUAGES

# Load environment variables (.env file if present)
dotenv.load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Effort-Aware AI Framework",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Modern Glassmorphic EdTech CSS Token System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #0B0F17;
        color: #F1F5F9;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.9) 50%, rgba(37, 99, 235, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        color: #CBD5E1;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 400;
    }
    .hero-badges {
        display: flex;
        gap: 0.8rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .badge-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #E2E8F0;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 500;
    }

    .glass-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .score-card-hero {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .score-number {
        font-size: 3.2rem;
        font-weight: 800;
        color: #38BDF8;
        letter-spacing: -0.03em;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .badge-level-1 {
        background: #1E3A8A;
        color: #93C5FD;
        border: 1px solid #3B82F6;
        padding: 0.5rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-level-2 {
        background: #78350F;
        color: #FDE68A;
        border: 1px solid #F59E0B;
        padding: 0.5rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-level-3 {
        background: #064E3B;
        color: #A7F3D0;
        border: 1px solid #10B981;
        padding: 0.5rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }

    .prog-bar-container {
        margin-bottom: 0.8rem;
    }
    .prog-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 0.25rem;
    }
    .prog-track {
        background: #1E293B;
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
    }
    .prog-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.4s ease;
    }

    .stTextArea textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 0.92rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    .chat-bubble-user {
        background: #1E293B;
        border: 1px solid #334155;
        color: #F1F5F9;
        padding: 0.9rem 1.2rem;
        border-radius: 12px 12px 2px 12px;
        margin-bottom: 0.8rem;
        margin-left: 2rem;
    }
    .chat-bubble-copilot {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        border: 1px solid #4338CA;
        color: #F8FAFC;
        padding: 1.1rem 1.3rem;
        border-radius: 12px 12px 12px 2px;
        margin-bottom: 0.8rem;
        margin-right: 2rem;
    }

    .stButton>button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "qb" not in st.session_state:
    st.session_state.qb = QuestionBank()

if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()

if "effort_engine" not in st.session_state:
    st.session_state.effort_engine = EffortEngine()

if "copilot_history" not in st.session_state:
    st.session_state.copilot_history = []

if "active_attempt" not in st.session_state:
    st.session_state.active_attempt = None

if "current_question_id" not in st.session_state:
    st.session_state.current_question_id = "q1"

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "Python"

# Hero Banner
st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">{APP_ICON} {APP_NAME}</div>
    <div class="hero-subtitle">{APP_SUBTITLE}</div>
    <div class="hero-badges">
        <span class="badge-pill">⚡ Effort Metric: E = 0.30A + 0.25C + 0.25R + 0.20T</span>
        <span class="badge-pill">🛡️ Safe Static Analysis</span>
        <span class="badge-pill">🤖 Dual AI Engine + Offline Fallback</span>
        <span class="badge-pill">🔑 Session: {st.session_state.session_id}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Workspace Controls")
    
    mode = st.radio(
        "Select Operating Mode",
        ["🎯 Problem Bank Mode", "✏️ Custom Problem Builder", "🤖 AI Copilot Chat Assistant"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🌐 Language & AI Config")
    selected_lang = st.selectbox("Target Programming Language", SUPPORTED_LANGUAGES, index=0)
    st.session_state.selected_language = selected_lang
    
    api_key_input = st.text_input("Gemini API Key (Optional)", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.caption("If Gemini API Key is unconfigured, the tutor seamlessly runs using the deterministic offline fallback engine.")

# Main Operational Views

if mode == "🎯 Problem Bank Mode" or mode == "✏️ Custom Problem Builder":
    
    if mode == "🎯 Problem Bank Mode":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📌 Filter Problems")
        
        topics = ["All"] + st.session_state.qb.get_topics()
        selected_topic = st.sidebar.selectbox("Topic Filter", topics)
        
        difficulties = ["All"] + st.session_state.qb.get_difficulties()
        selected_difficulty = st.sidebar.selectbox("Difficulty Filter", difficulties)
        
        filtered_q = st.session_state.qb.filter(topic=selected_topic, difficulty=selected_difficulty)
        
        if not filtered_q:
            st.warning("No questions match the selected filter.")
            st.stop()
            
        q_options = {f"{q.id}: {q.title} ({q.difficulty})": q.id for q in filtered_q}
        selected_label = st.sidebar.selectbox("Choose Problem", list(q_options.keys()))
        current_q = st.session_state.qb.get_by_id(q_options[selected_label])
        
    else: # Custom Problem Builder
        st.markdown("### ✏️ Custom Problem Definition")
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            custom_title = st.text_input("Custom Problem Title", value="My Custom Array Algorithm")
            custom_topic = st.text_input("Topic Category", value="Arrays & Hashing")
        with c_col2:
            custom_diff = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            custom_constraints = st.text_input("Constraints", value="1 <= N <= 10^5")
            
        custom_desc = st.text_area("Problem Statement & Description", value="Write a function that finds the first duplicate number in an array.", height=80)
        custom_ex_in = st.text_input("Example Input", value="arr = [2, 5, 1, 2, 3]")
        custom_ex_out = st.text_input("Example Output", value="2")
        custom_starter = st.text_area("Starter Code Template", value="def find_first_duplicate(arr):\n    # Write your solution here\n    pass", height=80)
        
        custom_q_dict = {
            "id": f"custom_{uuid.uuid4().hex[:6]}",
            "title": custom_title,
            "topic": custom_topic,
            "difficulty": custom_diff,
            "description": custom_desc,
            "constraints": custom_constraints,
            "example_input": custom_ex_in,
            "example_output": custom_ex_out,
            "starter_code": {selected_lang: custom_starter},
            "reference_solution": {selected_lang: f"# Custom Reference\n{custom_starter.replace('pass', '# Implementation')} "},
            "hints": ["Consider using a Hash Set to track seen elements in O(1) time.", "Iterate through elements and check if element exists in seen set."],
            "guided_steps": ["Step 1: Initialize an empty set `seen = set()`.", "Step 2: Loop over array elements.", "Step 3: If element in seen, return element.", "Step 4: Else add to seen."],
            "followup_question": "What is the time and space complexity of using a Hash Set vs nested loops?",
            "followup_options": ["Hash Set: O(N) time & O(N) space; Nested loops: O(N^2) time & O(1) space", "Both are O(N^2)", "Both are O(1)", "Nested loops are faster"],
            "followup_correct_index": 0
        }
        current_q = Question(custom_q_dict)

    col_left, col_right = st.columns([1.15, 0.85])

    with col_left:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">📌 {current_q.title}</div>
            <p><strong>Topic:</strong> <span class="badge-pill">{current_q.topic}</span> &nbsp;|&nbsp; <strong>Difficulty:</strong> <span class="badge-pill">{current_q.difficulty}</span></p>
            <hr style="border-color: #1F2937; margin: 0.8rem 0;"/>
            <p style="color: #E2E8F0; font-size: 0.95rem;">{current_q.description}</p>
            <p><strong>Constraints:</strong> <code style="color:#38BDF8">{current_q.constraints}</code></p>
            <p><strong>Example Input:</strong> <code style="color:#A7F3D0">{current_q.example_input}</code> &nbsp;|&nbsp; <strong>Output:</strong> <code style="color:#FDE68A">{current_q.example_output}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"#### 💻 Solution Code Editor (`{selected_lang}`)")
        default_starter = current_q.starter_code.get(selected_lang, f"# Write your {selected_lang} solution here\n")
        
        student_code = st.text_area(
            "Student Code Input",
            value=default_starter,
            height=240,
            key=f"editor_{current_q.id}_{selected_lang}",
            label_visibility="collapsed"
        )
        
        st.markdown("#### 💡 Thought Process & Reasoning Explanation")
        reasoning_text = st.text_area(
            "Explain your logic, variable choices, algorithm steps, and edge cases:",
            height=100,
            placeholder="e.g. First I initialized a counter to 0, then used a for loop to iterate through elements checking if...",
            key=f"reasoning_{current_q.id}"
        )
        
        st.markdown("#### 🧪 Debugging & Test Activity Notes")
        test_notes = st.text_area(
            "List test inputs tried, expected vs actual outputs, or error logs observed:",
            height=80,
            placeholder="e.g. Tested input arr=[2,5,1,2,3], expected 2, got 2. Edge case empty array tested...",
            key=f"test_notes_{current_q.id}"
        )

        st.markdown("#### ⚡ Actions")
        b1, b2, b3, b4 = st.columns(4)
        
        action_type = None
        forced_level = None
        
        with b1:
            if st.button("🚀 Submit & Evaluate", width="stretch", type="primary"):
                action_type = "Submit Attempt"
        with b2:
            if st.button("💡 Level 1 Hint", width="stretch"):
                action_type = "Get Hint"
                forced_level = 1
        with b3:
            if st.button("🛠️ Level 2 Guided", width="stretch"):
                action_type = "Guided Help"
                forced_level = 2
        with b4:
            if st.button("📖 Level 3 Solution", width="stretch"):
                action_type = "Full Solution"
                forced_level = 3

    with col_right:
        st.markdown("### 📊 Effort Evaluation & Assistance")
        
        if action_type:
            effort_res = st.session_state.effort_engine.evaluate(
                student_code=student_code,
                starter_code=default_starter,
                reasoning_text=reasoning_text,
                test_notes=test_notes,
                force_assistance_level=forced_level
            )
            
            tutor = TutorEngine(api_key=os.getenv("GEMINI_API_KEY"))
            tutor_resp = tutor.get_assistance(
                question=current_q,
                student_code=student_code,
                reasoning_text=reasoning_text,
                test_notes=test_notes,
                effort_result=effort_res,
                language=selected_lang
            )
            
            attempt_record = {
                "session_id": st.session_state.session_id,
                "question_id": current_q.id,
                "language": selected_lang,
                "attempt_number": 1,
                "student_code": student_code,
                "reasoning_text": reasoning_text,
                "test_notes": test_notes,
                "effort_score": effort_res.total_score,
                "score_A": effort_res.breakdown["A"],
                "score_C": effort_res.breakdown["C"],
                "score_R": effort_res.breakdown["R"],
                "score_T": effort_res.breakdown["T"],
                "assistance_level": effort_res.assistance_level,
                "assistance_type_requested": action_type,
                "tutor_response": tutor_resp["content"]
            }
            attempt_id = st.session_state.db.record_attempt(attempt_record)
            
            st.session_state.active_attempt = {
                "id": attempt_id,
                "effort_result": effort_res,
                "tutor_response": tutor_resp
            }

        if st.session_state.active_attempt:
            res = st.session_state.active_attempt["effort_result"]
            t_resp = st.session_state.active_attempt["tutor_response"]
            
            badge_cls = f"badge-level-{res.assistance_level}"
            st.markdown(f"""
            <div class="score-card-hero">
                <div style="font-size:0.85rem; color:#94A3B8; text-transform:uppercase; font-weight:600;">Evaluated Effort Proxy Score</div>
                <div class="score-number">{res.total_score:.1f} <span style="font-size:1.2rem; color:#64748B;">/ 100</span></div>
                <div class="{badge_cls}">{res.level_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"📌 **Pedagogical Rationale:**\n{res.recommendation_reason}")
            
            st.markdown("##### 🔍 Score Component Breakdown")
            
            comp_data = [
                ("Attempt Completeness (A - 30%)", res.breakdown['A'], "#3B82F6", res.explanations['A']),
                ("Code Modification Variance (C - 25%)", res.breakdown['C'], "#F59E0B", res.explanations['C']),
                ("Reasoning Depth (R - 25%)", res.breakdown['R'], "#10B981", res.explanations['R']),
                ("Test Engagement (T - 20%)", res.breakdown['T'], "#8B5CF6", res.explanations['T']),
            ]
            
            for name, val, color, desc in comp_data:
                st.markdown(f"""
                <div class="prog-bar-container">
                    <div class="prog-label"><span>{name}</span><strong>{val:.1f}%</strong></div>
                    <div class="prog-track"><div class="prog-fill" style="width:{val}%; background-color:{color};"></div></div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            if t_resp.get("info_note"):
                st.warning(f"ℹ️ {t_resp['info_note']}")
                
            st.markdown(f"**Provider:** `{t_resp['provider']}`")
            st.markdown(t_resp["content"])
            
            st.markdown("---")
            st.subheader("❓ Follow-up Concept Quiz")
            st.write(f"**Question:** {current_q.followup_question}")
            
            selected_option = st.radio(
                "Select your answer:",
                current_q.followup_options,
                key=f"quiz_{current_q.id}_{st.session_state.active_attempt['id']}"
            )
            
            if st.button("Submit Answer"):
                chosen_index = current_q.followup_options.index(selected_option)
                is_correct = (chosen_index == current_q.followup_correct_index)
                st.session_state.db.update_followup(st.session_state.active_attempt['id'], is_correct)
                
                if is_correct:
                    st.success("🎉 Correct! Excellent understanding of the underlying concept.")
                else:
                    correct_opt = current_q.followup_options[current_q.followup_correct_index]
                    st.error(f"❌ Incorrect. The correct answer is: **{correct_opt}**.")
        else:
            st.info("👈 Complete your solution code and reasoning on the left, then click **Submit & Evaluate**!")

elif mode == "🤖 AI Copilot Chat Assistant":
    st.markdown("### 🤖 AI Programming Copilot & Assistant")
    st.write("Ask any open-ended question about algorithms, syntax, debugging error messages, or custom code snippets.")

    tutor = TutorEngine(api_key=os.getenv("GEMINI_API_KEY"))

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.copilot_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user"><strong>👤 Student:</strong><br/>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-copilot"><strong>🤖 AI Copilot ({msg.get("provider", "Assistant")}):</strong><br/>{msg["content"]}</div>', unsafe_allow_html=True)

    with st.form("copilot_form", clear_on_submit=True):
        copilot_input = st.text_area("Ask AI Copilot a question or paste code to debug:", height=100, placeholder="e.g. Can you explain how two-pointer technique works for reversing an array in O(1) space?")
        submitted = st.form_submit_button("Send to AI Copilot 🚀", type="primary", width="stretch")

    if submitted and copilot_input.strip():
        st.session_state.copilot_history.append({"role": "user", "content": copilot_input})
        
        copilot_resp = tutor.ask_copilot(
            user_prompt=copilot_input,
            code_context="",
            language=st.session_state.selected_language,
            chat_history=st.session_state.copilot_history
        )
        
        st.session_state.copilot_history.append({
            "role": "copilot",
            "content": copilot_resp["content"],
            "provider": copilot_resp.get("provider", "Assistant")
        })
        st.rerun()

    if st.button("🗑️ Clear Copilot Chat History"):
        st.session_state.copilot_history = []
        st.rerun()
