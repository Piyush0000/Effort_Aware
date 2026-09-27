"""
Research Analytics & Advanced Visualization Dashboard.
"""

import streamlit as st
import pandas as pd
from database import DatabaseManager
from analytics import AnalyticsManager

st.set_page_config(page_title="Research Analytics", page_icon="🔬", layout="wide")

# Modern Dark Glassmorphic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0B0F17; color: #F1F5F9; }
    
    .research-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #1E3A8A 100%);
        border: 1px solid #4338CA;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .cond-metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 1.3rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    .stat-badge {
        background: rgba(56, 189, 248, 0.1);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="research-header">
    <h2 style="color:#FFF; margin:0; font-size: 2.1rem; font-weight:800;">🔬 Research Analytics & Comparative Policy Evaluation</h2>
    <p style="color:#A5B4FC; margin-top:0.4rem; margin-bottom:0; font-size:1.05rem;">
        Controlled empirical assessment of Effort-Aware Adaptive Assistance vs Fixed Scaffolding vs Immediate Solution disclosure.
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "🔬 **Methodological & Ethical Note:** "
    "The visualizations below present quantitative evaluation metrics across 3 scaffolding policy conditions. "
    "To enable reproducible validation prior to institutional participant data collection, "
    "this panel dynamically renders controlled benchmark trial datasets."
)

db = DatabaseManager()
analytics = AnalyticsManager(db)

# Seed synthetic data if missing
synthetic_data = db.get_synthetic_experiment_data()
if not synthetic_data:
    db.seed_synthetic_experiment_data(count=90)
    synthetic_data = db.get_synthetic_experiment_data()

df_syn = pd.DataFrame(synthetic_data)

# Metric Summary Row
cond_a = df_syn[df_syn["condition_group"].str.contains("Condition A")]
cond_b = df_syn[df_syn["condition_group"].str.contains("Condition B")]
cond_c = df_syn[df_syn["condition_group"].str.contains("Condition C")]

a_effort, c_effort = cond_a['effort_score'].mean(), cond_c['effort_score'].mean()
a_acc, c_acc = cond_a['followup_correct'].mean() * 100.0, cond_c['followup_correct'].mean() * 100.0
effort_delta = c_effort - a_effort
acc_delta = c_acc - a_acc

st.subheader("📊 Primary Metric Performance Across Experimental Conditions")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="cond-metric-card" style="border-top: 4px solid #EF4444;">
        <h4 style="color:#FCA5A5; margin-top:0;">Condition A: Immediate Solution</h4>
        <p style="color:#94A3B8; font-size:0.85rem;">Control group with immediate code answers.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Avg Effort Proxy Score", f"{a_effort:.1f} / 100")
    st.metric("Concept Accuracy Rate", f"{a_acc:.1f}%")

with col2:
    st.markdown("""
    <div class="cond-metric-card" style="border-top: 4px solid #F59E0B;">
        <h4 style="color:#FDE68A; margin-top:0;">Condition B: Fixed Hints</h4>
        <p style="color:#94A3B8; font-size:0.85rem;">Static 3-step progressive hint sequence.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Avg Effort Proxy Score", f"{cond_b['effort_score'].mean():.1f} / 100")
    st.metric("Concept Accuracy Rate", f"{(cond_b['followup_correct'].mean()*100):.1f}%")

with col3:
    st.markdown("""
    <div class="cond-metric-card" style="border-top: 4px solid #10B981;">
        <h4 style="color:#A7F3D0; margin-top:0;">Condition C: Effort-Aware Adaptive</h4>
        <p style="color:#94A3B8; font-size:0.85rem;">Dynamic scaffolding matching score E.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Avg Effort Proxy Score", f"{c_effort:.1f} / 100", delta=f"+{effort_delta:.1f} vs Control")
    st.metric("Concept Accuracy Rate", f"{c_acc:.1f}%", delta=f"+{acc_delta:.1f}% vs Control")

st.markdown("---")

# Section 1: Multi-Metric Radar & Grouped Performance Charts
st.subheader("🕸️ 1. Multi-Dimensional Scaffolding Benchmark & Accuracy")
col_r1, col_r2 = st.columns([1, 1])

with col_r1:
    fig_radar = analytics.get_radar_comparison_chart(df_syn)
    st.plotly_chart(fig_radar, width="stretch")

with col_r2:
    fig_bar = analytics.get_grouped_performance_bar_chart(df_syn)
    st.plotly_chart(fig_bar, width="stretch")

st.markdown("---")

# Section 2: Task Duration Distribution & Learning Curve
st.subheader("⏱️ 2. Task Duration Density & Mastery Progress Curves")
col_d1, col_d2 = st.columns([1, 1])

with col_d1:
    fig_violin = analytics.get_completion_time_violin_chart(df_syn)
    st.plotly_chart(fig_violin, width="stretch")

with col_d2:
    fig_curve = analytics.get_attempts_to_mastery_curve(df_syn)
    st.plotly_chart(fig_curve, width="stretch")

st.markdown("---")

# Section 3: Descriptive Statistical Summary Table
st.subheader("📑 3. Quantitative Statistical Summary Table")

stat_summary = df_syn.groupby("condition_group").agg(
    Sample_Count=("id", "count"),
    Mean_Effort=("effort_score", lambda x: f"{x.mean():.2f} ± {x.std():.2f}"),
    Concept_Accuracy=("followup_correct", lambda x: f"{(x.mean()*100):.1f}%"),
    First_Attempt_Pass=("first_attempt_correct", lambda x: f"{(x.mean()*100):.1f}%"),
    Avg_Completion_Time_Sec=("completion_time_sec", lambda x: f"{x.mean():.1f}s")
).reset_index()

stat_summary.columns = [
    "Experimental Condition", "N (Trials)", "Effort Proxy Score (Mean ± SD)",
    "Concept Accuracy (%)", "First-Attempt Pass (%)", "Mean Task Duration"
]

st.dataframe(stat_summary, width="stretch")

st.markdown("---")

# Research Control Buttons
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("🔄 Regenerate Research Trial Dataset (N=120)"):
        db.seed_synthetic_experiment_data(count=120)
        st.success("Regenerated 120 synthetic trial records.")
        st.rerun()

with c_btn2:
    st.download_button(
        label="📥 Download Research Dataset (CSV)",
        data=df_syn.to_csv(index=False),
        file_name="effort_aware_tutor_research_dataset.csv",
        mime="text/csv"
    )
