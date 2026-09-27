"""
Unit Tests for Effort Engine.
"""

import pytest
from effort_engine import EffortEngine, EffortResult

def test_effort_engine_empty_inputs():
    engine = EffortEngine()
    result = engine.evaluate(
        student_code="",
        starter_code="",
        reasoning_text="",
        test_notes=""
    )
    assert isinstance(result, EffortResult)
    assert result.total_score == 0.0
    assert result.assistance_level == 1
    assert result.breakdown["A"] == 0.0
    assert result.breakdown["C"] == 0.0
    assert result.breakdown["R"] == 0.0
    assert result.breakdown["T"] == 0.0

def test_effort_engine_level_1_hint():
    engine = EffortEngine()
    result = engine.evaluate(
        student_code="def sum(a, b): return 0",
        starter_code="def sum(a, b): pass",
        reasoning_text="I tried returning 0.",
        test_notes=""
    )
    assert result.total_score < 35.0
    assert result.assistance_level == 1
    assert "Level 1" in result.level_name

def test_effort_engine_level_2_guided():
    engine = EffortEngine()
    code = "def is_prime(n):\n    if n <= 1: return False\n    return True"
    starter = "def is_prime(n):\n    pass"
    reasoning = "I checked if n is less than 1."
    test_notes = "Tried n = 1."

    result = engine.evaluate(
        student_code=code,
        starter_code=starter,
        reasoning_text=reasoning,
        test_notes=test_notes
    )
    assert 35.0 <= result.total_score < 70.0
    assert result.assistance_level == 2

def test_effort_engine_level_3_worked_solution():
    engine = EffortEngine()
    code = """
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
"""
    starter = "def is_prime(n):\n    pass"
    reasoning = (
        "I optimized primality checking up to square root of n. First checking 2 and 3, "
        "then stepping by 6 to skip multiples of 2 and 3. This brings time complexity to O(sqrt(n))."
    )
    test_notes = "Ran test cases: n=1 (False), n=2 (True), n=29 (True), n=100 (False). Checked edge cases."

    result = engine.evaluate(
        student_code=code,
        starter_code=starter,
        reasoning_text=reasoning,
        test_notes=test_notes
    )
    assert result.total_score >= 70.0
    assert result.assistance_level == 3

def test_effort_engine_forced_assistance_level():
    engine = EffortEngine()
    result = engine.evaluate(
        student_code="pass",
        starter_code="pass",
        force_assistance_level=3
    )
    assert result.assistance_level == 3
    assert "manually requested" in result.recommendation_reason

def test_effort_engine_boundary_clamping():
    engine = EffortEngine()
    long_code = "def foo():\n" + "\n".join([f"    x_{i} = {i} + 1" for i in range(100)]) + "\n    return x_99"
    long_reasoning = "loop if else array index return function " * 50
    long_notes = "test input output error bug fix " * 50

    result = engine.evaluate(
        student_code=long_code,
        starter_code="def foo(): pass",
        reasoning_text=long_reasoning,
        test_notes=long_notes
    )
    assert result.total_score <= 100.0
    assert all(v <= 100.0 for v in result.breakdown.values())
    assert all(v >= 0.0 for v in result.breakdown.values())
