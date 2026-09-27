"""
Unit Tests for Question Bank Module.
"""

import pytest
from question_bank import QuestionBank

def test_question_bank_loading():
    qb = QuestionBank()
    questions = qb.get_all()
    assert len(questions) >= 15

def test_question_bank_topics_and_difficulties():
    qb = QuestionBank()
    topics = qb.get_topics()
    assert len(topics) >= 5
    assert "Variables and data types" in topics or "Loops" in topics

    difficulties = qb.get_difficulties()
    assert "Beginner" in difficulties
    assert "Intermediate" in difficulties
    assert "Advanced" in difficulties

def test_question_bank_filtering():
    qb = QuestionBank()
    beginner_questions = qb.filter(difficulty="Beginner")
    assert len(beginner_questions) > 0
    assert all(q.difficulty == "Beginner" for q in beginner_questions)

def test_question_bank_get_by_id():
    qb = QuestionBank()
    q1 = qb.get_by_id("q1")
    assert q1 is not None
    assert q1.id == "q1"
    assert "Python" in q1.starter_code
    assert "Java" in q1.starter_code
    assert len(q1.hints) > 0
    assert len(q1.guided_steps) > 0
