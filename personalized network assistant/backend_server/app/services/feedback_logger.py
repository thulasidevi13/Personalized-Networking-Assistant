# app/services/feedback_logger.py

import json
from datetime import datetime
from pathlib import Path

FEEDBACK_FILE = Path("feedback.json")

def log_feedback(suggestion: str, action: str):
    """
    User ka 'like' ya 'dislike' feedback ek specific suggestion ke liye record karta hai.
    """
    # 3 fields capture karna: suggestion, action, aur timestamp
    entry = {
        "suggestion": suggestion,
        "feedback": action,
        "timestamp": datetime.now().isoformat()
    }
    
    # Same read-modify-write pattern (History Logger jaisa)
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
        
    data.append(entry)
    
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_feedback():
    """
    Saara saved feedback analytics ya UI ke liye return karta hai.
    """
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []