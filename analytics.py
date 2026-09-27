"""
Research Analytics & Advanced Visualization Engine using Plotly & Pandas.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager

class AnalyticsManager:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def _apply_dark_theme(self, fig: go.Figure, title: str = "") -> go.Figure:
        """Applies a publication-grade dark glassmorphic Plotly theme."""
        fig.update_layout(
            title=dict(text=title, font=dict(size=16, color="#F8FAFC", family="Inter, sans-serif")),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#CBD5E1", family="Inter, sans-serif"),
            margin=dict(t=50, b=40, l=40, r=40),
            legend=dict(
                bgcolor="rgba(17, 24, 39, 0.8)",
                bordercolor="#374151",
                borderwidth=1,
                font=dict(color="#E2E8F0", size=11)
            ),
            xaxis=dict(gridcolor="#1F2937", zerolinecolor="#374151"),
            yaxis=dict(gridcolor="#1F2937", zerolinecolor="#374151")
        )
        return fig

    def get_assistance_distribution_chart(self, attempts: List[Dict[str, Any]]) -> go.Figure:
        """Generates Pie/Donut Chart for Assistance Level Distribution."""
        if not attempts:
            fig = px.pie(title="No Attempt Data Available")
            return self._apply_dark_theme(fig, "No Data")

        df = pd.DataFrame(attempts)
        level_map = {
            1: "Level 1 (Conceptual Hint)",
            2: "Level 2 (Guided Assistance)",
            3: "Level 3 (Worked Solution)"
        }
        df["Level_Name"] = df["assistance_level"].map(level_map)
        counts = df["Level_Name"].value_counts().reset_index()
        counts.columns = ["Assistance Level", "Count"]

        fig = px.pie(
            counts,
            values="Count",
            names="Assistance Level",
            hole=0.45,
            color_discrete_sequence=["#38BDF8", "#F59E0B", "#10B981"]
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#111827', width=2)))
        return self._apply_dark_theme(fig, "Distribution of Selected Assistance Levels")

    def get_effort_score_history_chart(self, attempts: List[Dict[str, Any]]) -> go.Figure:
        """Generates Line Chart for Effort Proxy Score History over Time."""
        if not attempts:
            fig = px.line(title="No Data Available")
            return self._apply_dark_theme(fig, "No Data")

        df = pd.DataFrame(attempts)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        fig = px.line(
            df,
            x="timestamp",
            y="effort_score",
            color="language",
            markers=True,
            color_discrete_sequence=["#38BDF8", "#F59E0B"]
        )
        fig.add_hline(y=35, line_dash="dash", line_color="#F59E0B", annotation_text="Level 2 Threshold (35)", annotation_position="top right")
        fig.add_hline(y=70, line_dash="dash", line_color="#10B981", annotation_text="Level 3 Threshold (70)", annotation_position="top right")
        fig.update_yaxes(range=[0, 105])
        return self._apply_dark_theme(fig, "Student Effort Proxy Score Progression Over Time")

    def get_radar_comparison_chart(self, df_syn: pd.DataFrame) -> go.Figure:
        """Generates Multi-Metric Polar Radar Chart comparing experimental policies."""
        categories = [
            'Effort Proxy Score',
            'Concept Accuracy (%)',
            'First-Attempt Correct (%)',
            'Scaffolding Efficiency',
            'Time Economy Index'
        ]

        conditions = df_syn["condition_group"].unique()
        fig = go.Figure()

        colors = {
            "Condition A (Immediate Solution)": "#EF4444",
            "Condition B (Fixed Hints)": "#F59E0B",
            "Condition C (Effort-Aware Adaptive)": "#10B981"
        }

        for cond in conditions:
            sub = df_syn[df_syn["condition_group"] == cond]
            avg_effort = sub["effort_score"].mean()
            avg_followup = sub["followup_correct"].mean() * 100.0
            avg_first = sub["first_attempt_correct"].mean() * 100.0
            avg_scaffolding = max(0, 100 - (sub["hints_requested"].mean() * 25.0))
            avg_time_idx = max(0, min(100, 100 - ((sub["completion_time_sec"].mean() - 100) / 2)))

            r_vals = [avg_effort, avg_followup, avg_first, avg_scaffolding, avg_time_idx]
            r_vals.append(r_vals[0]) # Close loop

            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=categories + [categories[0]],
                fill='toself',
                name=cond,
                line_color=colors.get(cond, "#38BDF8"),
                opacity=0.65
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1F2937", linecolor="#374151"),
                angularaxis=dict(gridcolor="#1F2937", linecolor="#374151"),
                bgcolor="#111827"
            )
        )
        return self._apply_dark_theme(fig, "Multi-Metric Comparative Radar Benchmark")

    def get_grouped_performance_bar_chart(self, df_syn: pd.DataFrame) -> go.Figure:
        """Generates Grouped Bar Chart comparing Effort Score vs Concept Accuracy."""
        summary = df_syn.groupby("condition_group").agg(
            avg_effort=("effort_score", "mean"),
            std_effort=("effort_score", "std"),
            avg_accuracy=("followup_correct", lambda x: x.mean() * 100.0),
            std_accuracy=("followup_correct", lambda x: x.std() * 100.0)
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=summary["condition_group"],
            y=summary["avg_effort"],
            name="Mean Effort Score (0-100)",
            marker_color="#38BDF8",
            error_y=dict(type='data', array=summary["std_effort"] / 2.0, color="#7DD3FC")
        ))
        fig.add_trace(go.Bar(
            x=summary["condition_group"],
            y=summary["avg_accuracy"],
            name="Concept Accuracy Rate (%)",
            marker_color="#10B981",
            error_y=dict(type='data', array=summary["std_accuracy"] / 2.0, color="#6EE7B7")
        ))

        fig.update_layout(barmode='group', yaxis_range=[0, 100])
        return self._apply_dark_theme(fig, "Mean Effort Proxy Score vs Concept Accuracy (with Error Bars)")

    def get_completion_time_violin_chart(self, df_syn: pd.DataFrame) -> go.Figure:
        """Generates Violin + Box Combo Plot for Problem Completion Time Distribution."""
        fig = px.violin(
            df_syn,
            x="condition_group",
            y="completion_time_sec",
            color="condition_group",
            box=True,
            points="all",
            color_discrete_sequence=["#EF4444", "#F59E0B", "#10B981"]
        )
        fig.update_layout(yaxis_title="Task Duration (Seconds)")
        return self._apply_dark_theme(fig, "Task Completion Time Density & Quartile Distribution")

    def get_attempts_to_mastery_curve(self, df_syn: pd.DataFrame) -> go.Figure:
        """Generates Cumulative Learning Curve showing attempts needed to solve problem."""
        fig = go.Figure()
        
        colors = {
            "Condition A (Immediate Solution)": "#EF4444",
            "Condition B (Fixed Hints)": "#F59E0B",
            "Condition C (Effort-Aware Adaptive)": "#10B981"
        }

        for cond in df_syn["condition_group"].unique():
            sub = df_syn[df_syn["condition_group"] == cond]
            counts = sub["total_attempts"].value_counts().sort_index()
            cum_pct = (counts.cumsum() / len(sub)) * 100.0
            
            fig.add_trace(go.Scatter(
                x=cum_pct.index,
                y=cum_pct.values,
                mode='lines+markers',
                name=cond,
                line=dict(color=colors.get(cond, "#38BDF8"), width=3),
                marker=dict(size=8)
            ))

        fig.update_layout(
            xaxis_title="Number of Attempts Required",
            yaxis_title="Cumulative Completion (%)",
            yaxis_range=[0, 105],
            xaxis=dict(tickmode='linear', tick0=1, dtick=1)
        )
        return self._apply_dark_theme(fig, "Cumulative Mastery Curve Across Trial Attempts")

    def get_experiment_comparison_charts() -> Dict[str, go.Figure]:
        """Generates full suite of research experiment visual charts."""
        data = self.db.get_synthetic_experiment_data()
        if not data:
            self.db.seed_synthetic_experiment_data(count=90)
            data = self.db.get_synthetic_experiment_data()

        df_syn = pd.DataFrame(data)

        radar_fig = self.get_radar_comparison_chart(df_syn)
        bar_fig = self.get_grouped_performance_bar_chart(df_syn)
        violin_fig = self.get_completion_time_violin_chart(df_syn)
        curve_fig = self.get_attempts_to_mastery_curve(df_syn)

        return {
            "radar_chart": radar_fig,
            "bar_chart": bar_fig,
            "violin_chart": violin_fig,
            "curve_chart": curve_fig
        }
