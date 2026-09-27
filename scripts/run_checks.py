"""
Automated System Verification Script.
"""

import sys
import os
import subprocess

# Add root project dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from question_bank import QuestionBank
from database import DatabaseManager
from effort_engine import EffortEngine

def run_system_checks():
    print("=" * 60)
    print("      EFFORT-AWARE AI TUTOR -- SYSTEM VERIFICATION")
    print("=" * 60)

    # 1. Question Bank Verification
    print("\n[1/4] Verifying Question Bank...")
    qb = QuestionBank()
    all_q = qb.get_all()
    print(f"  [OK] Loaded {len(all_q)} questions from JSON bank.")
    assert len(all_q) >= 15, "Question bank must contain at least 15 questions."

    # 2. Effort Engine Verification
    print("\n[2/4] Verifying Effort Engine Scoring Logic...")
    engine = EffortEngine()
    res = engine.evaluate(
        student_code="def convert_celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32",
        starter_code="def convert_celsius_to_fahrenheit(celsius):\n    pass",
        reasoning_text="Used standard formula multiplying celsius by 9/5 and adding 32.",
        test_notes="Tested celsius = 25, got 77.0."
    )
    print(f"  [OK] Sample effort proxy score: {res.total_score:.2f}/100 -> {res.level_name}")

    # 3. Database Layer Verification
    print("\n[3/4] Verifying Database Schema & Storage Layer...")
    db = DatabaseManager()
    stats = db.get_summary_stats()
    print(f"  [OK] Database active. Total attempts recorded: {stats['total_attempts']}")

    # 4. Pytest Execution
    print("\n[4/4] Running Pytest Unit Test Suite...")
    python_exe = sys.executable
    result = subprocess.run([python_exe, "-m", "pytest"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("  [OK] All pytest unit tests PASSED successfully!")
    else:
        print("  [FAIL] Pytest failed!")
        print(result.stderr)
        sys.exit(1)

    print("=" * 60)
    print("      SYSTEM VERIFICATION COMPLETE: ALL CHECKS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    run_system_checks()
