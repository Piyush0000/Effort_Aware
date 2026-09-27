"""
Student Learning Dashboard Page — Modern EdTech Theme.
"""

import streamlit as st
import pandas as pd
from database import DatabaseManager
from analytics import AnalyticsManager

st.set_page_config(page_title="Learning Dashboard", page_icon="📈", layout="wide")

# Modern EdTech Dark Glassmorphic Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0B0F17; color: #F1F5F9; }
    
    .dashboard-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .metric-card-dark {
        background: #111827;
        border: 1px solid #1F2937;
        border-left: 4px solid #38BDF8;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .metric-title { font-size: 0.8rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; }
    .metric-val { font-size: 1.8rem; font-weight: 800; color: #F8FAFC; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-header">
    <h2 style="color:#FFF; margin:0;">📈 Student Learning Analytics Dashboard</h2>
    <p style="color:#93C5FD; margin-top:0.3rem; margin-bottom:0;">Track your attempt progress, effort score trajectory, and conceptual accuracy.</p>
</div>
""", unsafe_allow_html=True)

db = DatabaseManager()
analytics = AnalyticsManager(db)

session_id = st.session_state.get("session_id", "default_session")
attempts = db.get_attempts(session_id=session_id)
all_attempts = db.get_attempts()

if not attempts and not all_attempts:
    st.info("No practice attempts recorded yet. Head over to the **Learn** workspace to start solving problems!")
    st.stop()

display_attempts = attempts if attempts else all_attempts
if not attempts and all_attempts:
    st.warning("Displaying all stored local attempt records (Session filter returned no matches).")

# Metric Summary Cards
col1, col2, col3, col4 = st.columns(4)

total_attempts = len(display_attempts)
unique_q = len(set(a["question_id"] for a in display_attempts))
avg_effort = sum(a["effort_score"] for a in display_attempts) / total_attempts if total_attempts > 0 else 0.0

answered_followups = [a for a in display_attempts if a.get("followup_answered") == 1]
correct_followups = [a for a in answered_followups if a.get("followup_correct") == 1]
accuracy = (len(correct_followups) / len(answered_followups) * 100.0) if answered_followups else 0.0

with col1:
    st.markdown(f'<div class="metric-card-dark"><div class="metric-title">Total Attempts</div><div class="metric-val">{total_attempts}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card-dark"><div class="metric-title">Unique Questions</div><div class="metric-val">{unique_q}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card-dark"><div class="metric-title">Avg Effort Proxy</div><div class="metric-val">{avg_effort:.1f}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card-dark"><div class="metric-title">Concept Accuracy</div><div class="metric-val">{accuracy:.1f}%</div></div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Visualizations
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Assistance Level Distribution")
    fig_dist = analytics.get_assistance_distribution_chart(display_attempts)
    fig_dist.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827", font_color="#F1F5F9")
    st.plotly_chart(fig_dist, use_container_width=True)

with col_right:
    st.subheader("Effort Score Timeline")
    fig_time = analytics.get_effort_score_history_chart(display_attempts)
    fig_time.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827", font_color="#F1F5F9")
    st.plotly_chart(fig_time, use_container_width=True)

st.markdown("---")

# Attempts Data Table
st.subheader("📜 Recent Attempt History Log")
df_attempts = pd.DataFrame(display_attempts)
if not df_attempts.empty:
    cols_to_show = ["id", "question_id", "language", "effort_score", "assistance_level", "timestamp"]
    st.dataframe(
        df_attempts[[c for c in cols_to_show if c in df_attempts.columns]],
        use_container_width=True
    )

st.markdown("---")

# History Purge Control
with st.expander("🗑️ Local History Management"):
    st.warning("Clearing history will reset all recorded attempt metrics from your local SQLite database.")
    if st.button("Clear My Local Learning History", type="secondary"):
        deleted = db.clear_history(session_id=session_id)
        st.success(f"Cleared {deleted} attempt records.")
        st.rerun()
