"""
SQLite Database Storage Layer for Student Learning History & Research Analytics.
"""

import sqlite3
import os
import random
from typing import List, Dict, Any, Optional
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initialize database schema automatically if tables do not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                language TEXT NOT NULL,
                attempt_number INTEGER DEFAULT 1,
                student_code TEXT,
                reasoning_text TEXT,
                test_notes TEXT,
                effort_score REAL NOT NULL,
                score_A REAL NOT NULL,
                score_C REAL NOT NULL,
                score_R REAL NOT NULL,
                score_T REAL NOT NULL,
                assistance_level INTEGER NOT NULL,
                assistance_type_requested TEXT,
                tutor_response TEXT,
                followup_answered INTEGER DEFAULT 0,
                followup_correct INTEGER DEFAULT 0,
                student_feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS synthetic_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition_group TEXT NOT NULL,
                question_id TEXT NOT NULL,
                first_attempt_correct INTEGER DEFAULT 0,
                total_attempts INTEGER DEFAULT 1,
                hints_requested INTEGER DEFAULT 0,
                followup_correct INTEGER DEFAULT 0,
                effort_score REAL NOT NULL,
                completion_time_sec REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

    def record_attempt(self, record: Dict[str, Any]) -> int:
        """Records a student attempt using parameterized SQL query."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attempts (
                    session_id, question_id, language, attempt_number,
                    student_code, reasoning_text, test_notes,
                    effort_score, score_A, score_C, score_R, score_T,
                    assistance_level, assistance_type_requested, tutor_response,
                    followup_answered, followup_correct, student_feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("session_id", "default_session"),
                record.get("question_id", "q1"),
                record.get("language", "Python"),
                record.get("attempt_number", 1),
                record.get("student_code", ""),
                record.get("reasoning_text", ""),
                record.get("test_notes", ""),
                record.get("effort_score", 0.0),
                record.get("score_A", 0.0),
                record.get("score_C", 0.0),
                record.get("score_R", 0.0),
                record.get("score_T", 0.0),
                record.get("assistance_level", 1),
                record.get("assistance_type_requested", "Submit Attempt"),
                record.get("tutor_response", ""),
                record.get("followup_answered", 0),
                record.get("followup_correct", 0),
                record.get("student_feedback", "")
            ))
            conn.commit()
            return cursor.lastrowid

    def update_followup(self, attempt_id: int, correct: bool) -> None:
        """Updates follow-up question answer result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attempts
                SET followup_answered = 1, followup_correct = ?
                WHERE id = ?
            """, (1 if correct else 0, attempt_id))
            conn.commit()

    def get_attempts(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves attempt records, optionally filtered by session_id."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute("SELECT * FROM attempts WHERE session_id = ? ORDER BY timestamp DESC", (session_id,))
            else:
                cursor.execute("SELECT * FROM attempts ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculates aggregated metrics for analytics dashboard."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM attempts")
            total_attempts = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT question_id) FROM attempts")
            unique_questions = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(effort_score) FROM attempts")
            avg_score = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT assistance_level, COUNT(*) FROM attempts GROUP BY assistance_level")
            level_counts = dict(cursor.fetchall())

            cursor.execute("SELECT COUNT(*) FROM attempts WHERE followup_answered = 1")
            total_followups = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM attempts WHERE followup_answered = 1 AND followup_correct = 1")
            correct_followups = cursor.fetchone()[0]

            followup_accuracy = (correct_followups / total_followups * 100.0) if total_followups > 0 else 0.0

            return {
                "total_attempts": total_attempts,
                "unique_questions": unique_questions,
                "avg_effort_score": round(avg_score, 2),
                "level_counts": level_counts,
                "total_followups": total_followups,
                "correct_followups": correct_followups,
                "followup_accuracy": round(followup_accuracy, 1)
            }

    def seed_synthetic_experiment_data(self, count: int = 60) -> None:
        """Seeds clearly labeled synthetic experimental data for research demonstration."""
        conditions = ["Condition A (Immediate Solution)", "Condition B (Fixed Hints)", "Condition C (Effort-Aware Adaptive)"]
        questions = [f"q{i}" for i in range(1, 16)]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM synthetic_experiments")
            
            for _ in range(count):
                cond = random.choice(conditions)
                q_id = random.choice(questions)
                
                if cond == "Condition A (Immediate Solution)":
                    effort = random.uniform(10, 45)
                    first_correct = random.choice([0, 1]) if random.random() < 0.4 else 0
                    attempts = random.randint(1, 4)
                    hints = 0
                    followup_corr = 1 if random.random() < 0.45 else 0
                    comp_time = random.uniform(90, 240)
                elif cond == "Condition B (Fixed Hints)":
                    effort = random.uniform(30, 65)
                    first_correct = 1 if random.random() < 0.55 else 0
                    attempts = random.randint(1, 3)
                    hints = random.randint(1, 3)
                    followup_corr = 1 if random.random() < 0.60 else 0
                    comp_time = random.uniform(120, 300)
                else: # Condition C (Effort-Aware Adaptive)
                    effort = random.uniform(50, 92)
                    first_correct = 1 if random.random() < 0.75 else 0
                    attempts = random.randint(1, 2)
                    hints = random.randint(1, 2)
                    followup_corr = 1 if random.random() < 0.82 else 0
                    comp_time = random.uniform(150, 360)

                cursor.execute("""
                    INSERT INTO synthetic_experiments (
                        condition_group, question_id, first_attempt_correct,
                        total_attempts, hints_requested, followup_correct,
                        effort_score, completion_time_sec
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (cond, q_id, first_correct, attempts, hints, followup_corr, effort, comp_time))
            
            conn.commit()

    def get_synthetic_experiment_data(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM synthetic_experiments")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def clear_history(self, session_id: Optional[str] = None) -> int:
        """Clears local attempt history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute("DELETE FROM attempts WHERE session_id = ?", (session_id,))
            else:
                cursor.execute("DELETE FROM attempts")
            deleted = cursor.rowcount
            conn.commit()
            return deleted
