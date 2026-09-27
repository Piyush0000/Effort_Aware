"""
Unit Tests for Database Operations.
"""

import os
import tempfile
import gc
import pytest
from database import DatabaseManager

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = DatabaseManager(db_path=path)
    yield db
    del db
    gc.collect()
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass

def test_db_initialization(temp_db):
    attempts = temp_db.get_attempts()
    assert isinstance(attempts, list)
    assert len(attempts) == 0

def test_db_record_and_retrieve_attempt(temp_db):
    record = {
        "session_id": "test_session_123",
        "question_id": "q1",
        "language": "Python",
        "attempt_number": 1,
        "student_code": "def foo(): pass",
        "reasoning_text": "testing code",
        "test_notes": "no errors",
        "effort_score": 45.0,
        "score_A": 40.0,
        "score_C": 50.0,
        "score_R": 40.0,
        "score_T": 50.0,
        "assistance_level": 2,
        "assistance_type_requested": "Submit Attempt",
        "tutor_response": "Guided steps provided",
        "followup_answered": 1,
        "followup_correct": 1,
        "student_feedback": "Helpful"
    }

    row_id = temp_db.record_attempt(record)
    assert row_id > 0

    attempts = temp_db.get_attempts(session_id="test_session_123")
    assert len(attempts) == 1
    assert attempts[0]["question_id"] == "q1"
    assert attempts[0]["effort_score"] == 45.0

def test_db_summary_stats(temp_db):
    record = {
        "session_id": "session_a",
        "question_id": "q2",
        "language": "Java",
        "attempt_number": 1,
        "effort_score": 80.0,
        "score_A": 80.0, "score_C": 80.0, "score_R": 80.0, "score_T": 80.0,
        "assistance_level": 3,
        "followup_answered": 1,
        "followup_correct": 1
    }
    temp_db.record_attempt(record)

    stats = temp_db.get_summary_stats()
    assert stats["total_attempts"] == 1
    assert stats["unique_questions"] == 1
    assert stats["avg_effort_score"] == 80.0
    assert stats["followup_accuracy"] == 100.0

def test_db_synthetic_experiments_seeding(temp_db):
    temp_db.seed_synthetic_experiment_data(count=30)
    data = temp_db.get_synthetic_experiment_data()
    assert len(data) == 30
    assert "condition_group" in data[0]

def test_db_clear_history(temp_db):
    temp_db.record_attempt({"session_id": "s1", "question_id": "q1", "language": "Python", "effort_score": 10.0, "score_A":0, "score_C":0, "score_R":0, "score_T":0, "assistance_level": 1})
    deleted = temp_db.clear_history()
    assert deleted == 1
    assert len(temp_db.get_attempts()) == 0
