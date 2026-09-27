"""
Question Bank Loader and Helper Utilities.
"""

import json
import os
from typing import List, Dict, Any, Optional
from config import QUESTIONS_FILE

class Question:
    def __init__(self, data: Dict[str, Any]):
        self.id: str = data.get("id", "")
        self.title: str = data.get("title", "Untitled Question")
        self.topic: str = data.get("topic", "General")
        self.difficulty: str = data.get("difficulty", "Beginner")
        self.description: str = data.get("description", "")
        self.constraints: str = data.get("constraints", "")
        self.example_input: str = data.get("example_input", "")
        self.example_output: str = data.get("example_output", "")
        self.starter_code: Dict[str, str] = data.get("starter_code", {})
        self.reference_solution: Dict[str, str] = data.get("reference_solution", {})
        self.hints: List[str] = data.get("hints", [])
        self.guided_steps: List[str] = data.get("guided_steps", [])
        self.followup_question: str = data.get("followup_question", "")
        self.followup_options: List[str] = data.get("followup_options", [])
        self.followup_correct_index: int = data.get("followup_correct_index", 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "description": self.description,
            "constraints": self.constraints,
            "example_input": self.example_input,
            "example_output": self.example_output,
            "starter_code": self.starter_code,
            "reference_solution": self.reference_solution,
            "hints": self.hints,
            "guided_steps": self.guided_steps,
            "followup_question": self.followup_question,
            "followup_options": self.followup_options,
            "followup_correct_index": self.followup_correct_index
        }

class QuestionBank:
    def __init__(self, filepath: str = QUESTIONS_FILE):
        self.filepath = filepath
        self.questions: List[Question] = []
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Question bank file not found: {self.filepath}")
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.questions = [Question(q) for q in data]

    def get_all(self) -> List[Question]:
        return self.questions

    def get_by_id(self, question_id: str) -> Optional[Question]:
        for q in self.questions:
            if q.id == question_id:
                return q
        return None

    def get_topics(self) -> List[str]:
        topics = list(set(q.topic for q in self.questions))
        topics.sort()
        return topics

    def get_difficulties(self) -> List[str]:
        return ["Beginner", "Intermediate", "Advanced"]

    def filter(self, topic: Optional[str] = None, difficulty: Optional[str] = None) -> List[Question]:
        filtered = self.questions
        if topic and topic != "All":
            filtered = [q for q in filtered if q.topic == topic]
        if difficulty and difficulty != "All":
            filtered = [q for q in filtered if q.difficulty == difficulty]
        return filtered
