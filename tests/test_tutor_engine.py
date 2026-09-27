"""
Unit Tests for AI Tutor Engine, Copilot & Offline Fallback.
"""

import pytest
from question_bank import QuestionBank
from effort_engine import EffortEngine
from tutor_engine import OfflineTutorProvider, GeminiTutorProvider, TutorEngine

def test_offline_tutor_provider_level_1():
    qb = QuestionBank()
    question = qb.get_by_id("q1")
    assert question is not None

    engine = EffortEngine()
    effort_res = engine.evaluate(student_code="", starter_code="", reasoning_text="", test_notes="")
    
    provider = OfflineTutorProvider()
    res = provider.generate_assistance(
        question=question,
        student_code="",
        reasoning_text="",
        test_notes="",
        effort_result=effort_res,
        language="Python"
    )

    assert res["success"] is True
    assert res["level"] == 1
    assert "Conceptual Hint" in res["content"] or "Level 1" in res["content"]
    assert res["is_offline"] is True

def test_offline_tutor_provider_level_2():
    qb = QuestionBank()
    question = qb.get_by_id("q1")
    engine = EffortEngine()
    effort_res = engine.evaluate(
        student_code="def convert_celsius_to_fahrenheit(celsius):\n return celsius",
        starter_code="def convert_celsius_to_fahrenheit(celsius):\n pass",
        reasoning_text="I returned celsius directly.",
        test_notes="Output was 25 instead of 77",
        force_assistance_level=2
    )

    provider = OfflineTutorProvider()
    res = provider.generate_assistance(
        question=question,
        student_code="def convert_celsius_to_fahrenheit(celsius):\n return celsius",
        reasoning_text="I returned celsius directly.",
        test_notes="Output was 25 instead of 77",
        effort_result=effort_res,
        language="Python"
    )

    assert res["success"] is True
    assert res["level"] == 2
    assert "Guided Assistance" in res["content"] or "Level 2" in res["content"]

def test_offline_tutor_provider_level_3():
    qb = QuestionBank()
    question = qb.get_by_id("q1")
    engine = EffortEngine()
    effort_res = engine.evaluate(
        student_code="def convert_celsius_to_fahrenheit(celsius):\n return (celsius * 9/5) + 32",
        starter_code="",
        reasoning_text="Used exact mathematical conversion formula F = C * 9/5 + 32.",
        test_notes="Tested celsius 0 -> 32, 25 -> 77, 100 -> 212. All passed.",
        force_assistance_level=3
    )

    provider = OfflineTutorProvider()
    res = provider.generate_assistance(
        question=question,
        student_code="def convert_celsius_to_fahrenheit(celsius):\n return (celsius * 9/5) + 32",
        reasoning_text="Used exact formula",
        test_notes="All tests passed",
        effort_result=effort_res,
        language="Python"
    )

    assert res["success"] is True
    assert res["level"] == 3
    assert "WORKED SOLUTION" in res["content"] or "Reference Solution" in res["content"]

def test_copilot_ask_question_offline():
    tutor = TutorEngine(api_key=None)
    copilot_res = tutor.ask_copilot("How do I debug IndexOutOfBoundsException in Java?", language="Java")
    assert copilot_res["success"] is True
    assert "Copilot" in copilot_res["provider"] or "Offline" in copilot_res["provider"]
    assert "Debugging" in copilot_res["content"] or "Index" in copilot_res["content"]

def test_gemini_provider_without_api_key_graceful_fallback():
    qb = QuestionBank()
    question = qb.get_by_id("q1")
    engine = EffortEngine()
    effort_res = engine.evaluate(student_code="", starter_code="", reasoning_text="", test_notes="")

    gemini_provider = GeminiTutorProvider(api_key=None)
    res = gemini_provider.generate_assistance(
        question=question,
        student_code="",
        reasoning_text="",
        test_notes="",
        effort_result=effort_res,
        language="Python"
    )

    assert res["success"] is True
    assert res["is_offline"] is True
    assert "info_note" in res
