"""
AI Tutor Engine with Modular Provider Architecture, Custom Questions & AI Copilot.

Supports:
1. GeminiTutorProvider (Official google-genai Python SDK)
2. OfflineTutorProvider (Deterministic fallback using local question bank)
"""

import os
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from question_bank import Question
from effort_engine import EffortResult
from config import DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODELS

logger = logging.getLogger(__name__)

class BaseTutorProvider(ABC):
    @abstractmethod
    def generate_assistance(
        self,
        question: Question,
        student_code: str,
        reasoning_text: str,
        test_notes: str,
        effort_result: EffortResult,
        language: str = "Python"
    ) -> Dict[str, Any]:
        """Generates scaffolded pedagogical assistance based on effort level."""
        pass

    @abstractmethod
    def ask_copilot(
        self,
        user_prompt: str,
        code_context: str = "",
        language: str = "Python",
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Answers arbitrary student programming and copilot questions."""
        pass

class OfflineTutorProvider(BaseTutorProvider):
    """Deterministic offline provider when API keys are unavailable or offline mode is requested."""

    def generate_assistance(
        self,
        question: Question,
        student_code: str,
        reasoning_text: str,
        test_notes: str,
        effort_result: EffortResult,
        language: str = "Python"
    ) -> Dict[str, Any]:
        level = effort_result.assistance_level
        ref_sol = question.reference_solution.get(language, "No reference solution available for this language.")

        if level == 1:
            hints_str = "\n".join(f"• {h}" for h in question.hints) if question.hints else "• Identify inputs and outputs.\n• Break problem into logical steps."
            response_text = (
                f"### 💡 Conceptual Hint (Level 1 — HINT)\n\n"
                f"**Pedagogical Scaffolding:**\n"
                f"Your evaluated effort proxy score is **{effort_result.total_score:.1f}/100**. "
                f"To encourage independent thinking, here are key conceptual pointers:\n\n"
                f"{hints_str}\n\n"
                f"**Action Plan:**\n"
                f"Try writing down the algorithm steps in plain text before coding."
            )
        elif level == 2:
            steps_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(question.guided_steps)) if question.guided_steps else "1. Parse inputs.\n2. Execute loop logic.\n3. Return result."
            starter = question.starter_code.get(language, "# Starter code skeleton")
            response_text = (
                f"### 🛠️ Guided Assistance & Pseudocode (Level 2 — GUIDED)\n\n"
                f"**Algorithmic Sequence:**\n"
                f"{steps_str}\n\n"
                f"**Code Skeleton ({language}):**\n"
                f"```{language.lower()}\n{starter}\n```\n\n"
                f"**Next Step:**\n"
                f"Fill in the missing loop condition and return statement."
            )
        else:
            response_text = (
                f"### 📖 Full Reference Solution & Complexity Analysis (Level 3 — WORKED SOLUTION)\n\n"
                f"**Complete Implementation ({language}):**\n"
                f"```{language.lower()}\n{ref_sol}\n```\n\n"
                f"**Line-by-Line Breakdown:**\n"
                f"The reference code efficiently solves `{question.title}` handling boundary conditions.\n\n"
                f"**Complexity Analysis:**\n"
                f"- **Time Complexity:** $O(N)$ linear pass or $O(1)$ constant.\n"
                f"- **Space Complexity:** $O(1)$ auxiliary memory."
            )

        return {
            "success": True,
            "provider": "Offline Fallback Engine",
            "content": response_text,
            "level": level,
            "is_offline": True,
            "error_message": None
        }

    def ask_copilot(
        self,
        user_prompt: str,
        code_context: str = "",
        language: str = "Python",
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Offline Copilot response using intelligent template matching."""
        prompt_lower = user_prompt.lower()
        
        if "error" in prompt_lower or "debug" in prompt_lower or "bug" in prompt_lower:
            reply = (
                f"### 🐞 AI Copilot Debugging Advice ({language})\n\n"
                f"I reviewed your query regarding: *\"{user_prompt}\"*\n\n"
                f"**Common Debugging Checklist:**\n"
                f"1. **Index Out of Bounds:** Verify loop boundary limits (`len(arr) - 1` vs `len(arr)`).\n"
                f"2. **Type Discrepancy:** Ensure variables are properly cast (e.g. `int()`, `float()`, `String`).\n"
                f"3. **Return Location:** Make sure `return` is placed outside the inner loop.\n\n"
                f"```python\n# Tip: Add print statements to trace variable values\nprint(f'Debug trace: val={code_context[:50]}...')\n```"
            )
        elif "time complexity" in prompt_lower or "big o" in prompt_lower or "space" in prompt_lower:
            reply = (
                f"### ⏱️ Time & Space Complexity Copilot\n\n"
                f"**Key Complexity Rules:**\n"
                f"- Single loop over $N$ items $\\implies O(N)$ time.\n"
                f"- Two nested loops over $N$ items $\\implies O(N^2)$ time.\n"
                f"- Binary search / dividing problem size in half $\\implies O(\\log N)$ time.\n\n"
                f"*Offline Note: Connect Gemini API Key in sidebar for full dynamic LLM responses.*"
            )
        else:
            reply = (
                f"### 🤖 AI Copilot Assistant\n\n"
                f"**Question:** {user_prompt}\n\n"
                f"**Copilot Guidance:**\n"
                f"Great question! When tackling `{language}` problems, always begin by specifying:\n"
                f"1. What are the input constraints?\n"
                f"2. What is the expected return type?\n"
                f"3. Are there edge cases (e.g., empty array, zero, negative numbers)?\n\n"
                f"```{language.lower()}\n# Sample snippet\ndef solve_problem(data):\n    # Implement core algorithm step by step\n    pass\n```"
            )

        return {
            "success": True,
            "provider": "Offline Copilot Assistant",
            "content": reply,
            "is_offline": True
        }

class GeminiTutorProvider(BaseTutorProvider):
    """Google Gemini AI Provider via official google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_GEMINI_MODEL):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client: {e}")

    def _generate(self, prompt: str):
        """Calls Gemini, retrying transient errors (overload / rate limit) and trying backup models."""
        models = [self.model_name] + [m for m in FALLBACK_GEMINI_MODELS if m != self.model_name]
        last_error = None
        for model in models:
            for attempt in range(2):
                try:
                    response = self.client.models.generate_content(model=model, contents=prompt)
                    if response and response.text:
                        return response.text, model
                    raise ValueError("Empty response returned from Gemini API.")
                except Exception as e:
                    last_error = e
                    msg = str(e)
                    if not any(code in msg for code in ("503", "429", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                        break  # not transient: move on to the next model
                    logger.warning(f"Gemini {model} attempt {attempt + 1} failed: {e}")
                    time.sleep(1.5 * (attempt + 1))
        raise last_error

    def generate_assistance(
        self,
        question: Question,
        student_code: str,
        reasoning_text: str,
        test_notes: str,
        effort_result: EffortResult,
        language: str = "Python"
    ) -> Dict[str, Any]:
        offline_fallback = OfflineTutorProvider()

        if not self.api_key or not self.client:
            res = offline_fallback.generate_assistance(question, student_code, reasoning_text, test_notes, effort_result, language)
            res["info_note"] = "Gemini API key not configured. Using deterministic offline fallback engine."
            return res

        level = effort_result.assistance_level

        level_rules = {
            1: "LEVEL 1 RULES: Provide ONLY high-level conceptual hints and next steps. Do NOT write full code solutions or reveal the complete answer.",
            2: "LEVEL 2 RULES: Provide structured algorithmic steps, pseudocode, or partial code snippets. Do NOT provide a 100% complete copy-pasteable solution.",
            3: "LEVEL 3 RULES: Provide a complete, production-grade reference solution, line-by-line explanation, and detailed time/space complexity analysis."
        }

        prompt = f"""
You are an expert, encouraging, and effort-aware computer science educator.

[PROBLEM SPECIFICATION]
Title: {question.title}
Topic: {question.topic}
Difficulty: {question.difficulty}
Description: {question.description}
Constraints: {question.constraints}
Example Input: {question.example_input}
Example Output: {question.example_output}

[STUDENT ATTEMPT]
Programming Language: {language}
Student Code:
```{language.lower()}
{student_code if student_code.strip() else "(No code submitted)"}
```

Student Reasoning / Explanation:
{reasoning_text if reasoning_text.strip() else "(No reasoning provided)"}

Student Test Notes / Debugging Activity:
{test_notes if test_notes.strip() else "(No test notes provided)"}

[EVALUATED EFFORT PROXY & PEDAGOGICAL POLICY]
Calculated Effort Proxy Score: {effort_result.total_score}/100
Selected Assistance Level: Level {level} - {effort_result.level_name}
Reason: {effort_result.recommendation_reason}

[STRICT SCAFFOLDING GUIDELINES]
{level_rules.get(level, level_rules[1])}

Important Constraints:
- Do NOT invent or fabricate execution outputs or compiler errors.
- Tone: Encouraging, supportive, clear, academic.
- Format using rich GFM markdown headers, bullet points, and code blocks.
"""

        try:
            text, model_used = self._generate(prompt)
            return {
                "success": True,
                "provider": f"Google Gemini ({model_used})",
                "content": text,
                "level": level,
                "is_offline": False,
                "error_message": None
            }

        except Exception as e:
            logger.error(f"Gemini API invocation error: {e}")
            res = offline_fallback.generate_assistance(question, student_code, reasoning_text, test_notes, effort_result, language)
            res["info_note"] = f"Gemini API call failed ({str(e)}). Switched to offline fallback engine."
            return res

    def ask_copilot(
        self,
        user_prompt: str,
        code_context: str = "",
        language: str = "Python",
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Generates real-time AI Copilot answers using Gemini API."""
        offline_fallback = OfflineTutorProvider()

        if not self.api_key or not self.client:
            return offline_fallback.ask_copilot(user_prompt, code_context, language, chat_history)

        prompt = f"""
You are an intelligent, friendly AI Programming Copilot and CS Mentor.
The student is working in {language}.

[STUDENT CODE CONTEXT]
```{language.lower()}
{code_context if code_context.strip() else "(No active code)"}
```

[STUDENT QUESTION]
{user_prompt}

Guidelines:
- Provide clear, concise, step-by-step explanations.
- Include short, well-commented code snippets where relevant.
- Do not make up fake library functions or compiler errors.
- Format with clean GitHub Flavored Markdown.
"""

        try:
            text, model_used = self._generate(prompt)
            return {
                "success": True,
                "provider": f"Google Gemini Copilot ({model_used})",
                "content": text,
                "is_offline": False
            }
        except Exception as e:
            logger.error(f"Gemini Copilot API error: {e}")
            return offline_fallback.ask_copilot(user_prompt, code_context, language, chat_history)

class TutorEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.provider = GeminiTutorProvider(api_key=self.api_key)
        else:
            self.provider = OfflineTutorProvider()

    def get_assistance(
        self,
        question: Question,
        student_code: str,
        reasoning_text: str,
        test_notes: str,
        effort_result: EffortResult,
        language: str = "Python"
    ) -> Dict[str, Any]:
        return self.provider.generate_assistance(
            question=question,
            student_code=student_code,
            reasoning_text=reasoning_text,
            test_notes=test_notes,
            effort_result=effort_result,
            language=language
        )

    def ask_copilot(
        self,
        user_prompt: str,
        code_context: str = "",
        language: str = "Python",
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        return self.provider.ask_copilot(
            user_prompt=user_prompt,
            code_context=code_context,
            language=language,
            chat_history=chat_history
        )
