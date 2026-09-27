"""
Effort Proxy Engine for Observable Engagement & Attempt Analysis.

Calculates an explainable observable effort/attempt proxy score (E) bounded [0, 100]:
Formula: E = 0.30 * A + 0.25 * C + 0.25 * R + 0.20 * T

Where:
  A = Attempt Completeness Score (0-100)
  C = Meaningful Code Modification Score (0-100)
  R = Reasoning Explanation Completeness Score (0-100)
  T = Debugging & Test Engagement Score (0-100)

IMPORTANT RESEARCH NOTE:
This score is an observable behavioral interaction proxy metric designed to inform
scaffolded pedagogical assistance. It does NOT claim to measure innate intelligence,
cognitive capacity, or intrinsic student motivation.
"""

import re
import difflib
from typing import Dict, Any, Optional
from config import EFFORT_WEIGHTS, LEVEL_THRESHOLDS, ASSISTANCE_LEVELS

class EffortResult:
    def __init__(
        self,
        total_score: float,
        assistance_level: int,
        level_name: str,
        breakdown: Dict[str, float],
        explanations: Dict[str, str],
        recommendation_reason: str
    ):
        self.total_score = round(max(0.0, min(100.0, total_score)), 2)
        self.assistance_level = assistance_level
        self.level_name = level_name
        self.breakdown = {k: round(max(0.0, min(100.0, v)), 2) for k, v in breakdown.items()}
        self.explanations = explanations
        self.recommendation_reason = recommendation_reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_score": self.total_score,
            "assistance_level": self.assistance_level,
            "level_name": self.level_name,
            "breakdown": self.breakdown,
            "explanations": self.explanations,
            "recommendation_reason": self.recommendation_reason
        }

class EffortEngine:
    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None
    ):
        self.weights = weights or EFFORT_WEIGHTS
        self.thresholds = thresholds or LEVEL_THRESHOLDS

    def calculate_attempt_completeness(self, student_code: str, starter_code: str) -> tuple[float, str]:
        """Calculates Attempt Completeness Score (A)."""
        if not student_code or not student_code.strip():
            return 0.0, "No code submission detected."

        code_lines = [line.strip() for line in student_code.splitlines() if line.strip() and not line.strip().startswith("#")]
        num_lines = len(code_lines)

        # Base score on line count and code constructs
        base_score = min(50.0, num_lines * 7.5)

        # Check for key structural constructs (control flow, functions, returns)
        has_func = bool(re.search(r'\b(def|public|class|static|return)\b', student_code))
        has_logic = bool(re.search(r'\b(if|else|for|while|try|catch)\b', student_code))
        has_assign = bool(re.search(r'(=|\+=|-=|\*=)', student_code))

        construct_score = 0.0
        if has_func: construct_score += 20.0
        if has_logic: construct_score += 20.0
        if has_assign: construct_score += 10.0

        score = min(100.0, base_score + construct_score)
        explanation = (
            f"Code contains {num_lines} non-comment lines. "
            f"Structure detects functions ({has_func}), control logic ({has_logic}), and state assignment ({has_assign})."
        )
        return score, explanation

    def calculate_code_modification(self, student_code: str, starter_code: str) -> tuple[float, str]:
        """Calculates Meaningful Code Modification Score (C)."""
        if not student_code or not student_code.strip():
            return 0.0, "No modifications evaluated on empty code."

        if not starter_code or not starter_code.strip():
            # If starter code was blank, any substantive code is a modification
            words = len(student_code.split())
            score = min(100.0, words * 4.0)
            return score, f"Starter code was empty; submission contains {words} words."

        # Normalized string comparison
        seq = difflib.SequenceMatcher(None, starter_code.strip(), student_code.strip())
        similarity = seq.ratio()
        diff_score = (1.0 - similarity) * 100.0

        # Reward removal of pass / return 0 placeholders
        placeholder_cleared = "pass" not in student_code and "return 0" not in student_code
        if placeholder_cleared and ("pass" in starter_code or "return 0" in starter_code):
            diff_score = min(100.0, diff_score + 25.0)

        score = min(100.0, max(0.0, diff_score))
        explanation = (
            f"Code diff ratio shows {round((1.0 - similarity) * 100, 1)}% variance from template. "
            f"Placeholder replacement bonus applied: {placeholder_cleared}."
        )
        return score, explanation

    def calculate_reasoning_completeness(self, reasoning_text: str) -> tuple[float, str]:
        """Calculates Reasoning Explanation Completeness Score (R)."""
        if not reasoning_text or not reasoning_text.strip():
            return 0.0, "No reasoning or thought-process explanation provided."

        words = reasoning_text.strip().split()
        word_count = len(words)

        # Word count contribution (concise explanations get fair baseline)
        length_score = min(60.0, word_count * 3.0)

        # Pedagogical domain keyword detection
        keywords = [
            "loop", "for", "while", "if", "else", "condition", "variable",
            "array", "index", "pointer", "return", "function", "compare",
            "check", "increment", "step", "base case", "recursion", "divide",
            "formula", "because", "so", "first", "then", "finally", "convert"
        ]

        found_keywords = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', reasoning_text, re.IGNORECASE)]
        kw_score = min(40.0, len(found_keywords) * 8.0)

        score = min(100.0, length_score + kw_score)
        explanation = (
            f"Reasoning contains {word_count} words and {len(found_keywords)} domain conceptual terms "
            f"({', '.join(found_keywords[:5])}{'...' if len(found_keywords) > 5 else ''})."
        )
        return score, explanation

    def calculate_test_engagement(self, test_notes: str) -> tuple[float, str]:
        """Calculates Debugging & Test Engagement Score (T)."""
        if not test_notes or not test_notes.strip():
            return 0.0, "No testing or debugging activity notes provided."

        words = len(test_notes.strip().split())
        length_score = min(50.0, words * 4.0)

        # Detect test signals (numbers, expected outputs, error messages, edge cases)
        has_test_values = bool(re.search(r'(\d+|input|output|test|case|expected|actual)', test_notes, re.IGNORECASE))
        has_error_notes = bool(re.search(r'(error|bug|fail|exception|wrong|traceback|fix)', test_notes, re.IGNORECASE))

        signal_score = 0.0
        if has_test_values: signal_score += 30.0
        if has_error_notes: signal_score += 20.0

        score = min(100.0, length_score + signal_score)
        explanation = (
            f"Test engagement contains {words} words. "
            f"Detected test value specifications ({has_test_values}) and debugging notes ({has_error_notes})."
        )
        return score, explanation

    def evaluate(
        self,
        student_code: str,
        starter_code: str = "",
        reasoning_text: str = "",
        test_notes: str = "",
        force_assistance_level: Optional[int] = None
    ) -> EffortResult:
        """Evaluates student submission and returns EffortResult."""
        # Calculate components safely
        score_A, exp_A = self.calculate_attempt_completeness(student_code, starter_code)
        score_C, exp_C = self.calculate_code_modification(student_code, starter_code)
        score_R, exp_R = self.calculate_reasoning_completeness(reasoning_text)
        score_T, exp_T = self.calculate_test_engagement(test_notes)

        # Weighted aggregate score E = 0.30*A + 0.25*C + 0.25*R + 0.20*T
        weighted_total = (
            self.weights["A"] * score_A +
            self.weights["C"] * score_C +
            self.weights["R"] * score_R +
            self.weights["T"] * score_T
        )

        total_score = max(0.0, min(100.0, weighted_total))

        # Determine Assistance Level
        if force_assistance_level in [1, 2, 3]:
            level = force_assistance_level
            level_reason = f"Level manually requested by student (Calculated Effort Score: {total_score:.1f}/100)."
        else:
            if total_score < self.thresholds["LEVEL_1_MAX"]:
                level = 1
                level_reason = (
                    f"Effort proxy score is {total_score:.1f}/100 (below threshold {self.thresholds['LEVEL_1_MAX']:.1f}). "
                    "Assigned Level 1 (Conceptual Hint) to encourage deeper independent exploration."
                )
            elif total_score < self.thresholds["LEVEL_2_MAX"]:
                level = 2
                level_reason = (
                    f"Effort proxy score is {total_score:.1f}/100 (between {self.thresholds['LEVEL_1_MAX']:.1f} and {self.thresholds['LEVEL_2_MAX']:.1f}). "
                    "Assigned Level 2 (Guided Assistance) providing algorithmic structure and pseudocode."
                )
            else:
                level = 3
                level_reason = (
                    f"Effort proxy score is {total_score:.1f}/100 (above threshold {self.thresholds['LEVEL_2_MAX']:.1f}). "
                    "Assigned Level 3 (Full Worked Solution) acknowledging thorough student effort."
                )

        level_name = ASSISTANCE_LEVELS.get(level, "Unknown Level")
        breakdown = {"A": score_A, "C": score_C, "R": score_R, "T": score_T}
        explanations = {"A": exp_A, "C": exp_C, "R": exp_R, "T": exp_T}

        return EffortResult(
            total_score=total_score,
            assistance_level=level,
            level_name=level_name,
            breakdown=breakdown,
            explanations=explanations,
            recommendation_reason=level_reason
        )
