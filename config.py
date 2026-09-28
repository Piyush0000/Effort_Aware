"""
Configuration settings for Effort-Aware Generative AI Framework.
"""

import os

# Application Metadata
APP_NAME = "Effort-Aware AI Framework"
APP_SUBTITLE = "Reducing Cognitive Offloading in Programming Education"
APP_ICON = "🎓"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "tutor_data.db")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")

# Effort Engine Weights & Thresholds
EFFORT_WEIGHTS = {
    "A": 0.30,  # Attempt completeness score (0-100)
    "C": 0.25,  # Meaningful code modification score (0-100)
    "R": 0.25,  # Reasoning explanation completeness score (0-100)
    "T": 0.20,  # Debugging and test engagement score (0-100)
}

# Configurable Level Thresholds
LEVEL_THRESHOLDS = {
    "LEVEL_1_MAX": 35.0,
    "LEVEL_2_MAX": 70.0
}

ASSISTANCE_LEVELS = {
    1: "Level 1 — HINT (Conceptual Clues & Next Steps)",
    2: "Level 2 — GUIDED (Algorithm, Pseudocode & Partial Code)",
    3: "Level 3 — WORKED SOLUTION (Complete Reference Code & Complexity)"
}

# Supported Languages
SUPPORTED_LANGUAGES = ["Python", "Java"]

# Gemini AI Settings
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
