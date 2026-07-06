# app/services/history_logger.py

import json
from datetime import datetime
from pathlib import Path

# pathlib.Path ka use (Cross-platform compatibility ke liye)
HISTORY_FILE = Path("history.json")

def log_conversation(data: dict):
    """
    ISO timestamp add karke conversation data ko JSON file mein append karta hai.
    """
    # 1. ISO-formatted timestamp add karna
    data["timestamp"] = datetime.now().isoformat()
    
    # 2. Read-modify-write pattern
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = [] # Agar file empty ya corrupt ho
    else:
        history = []
        
    # Naya data append karna
    history.append(data)
    
    # Updated list ko wapas disk par write karna
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def load_history() -> list:
    """
    History file ko read karke list return karta hai (file na hone par empty list).
    """
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    
    # Agar history save nahi hui hai toh clean empty list return karega
    return []