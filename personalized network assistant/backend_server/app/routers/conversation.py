# app/routers/conversation.py

from fastapi import APIRouter
from app.models.schemas import (
    EventInput, 
    ConversationRequest, 
    FactCheckRequest, 
    ConversationResponse, 
    FactCheckResponse
)

# Saari services ko import kar rahe hain
from app.services.event_analyzer import extract_event_themes
from app.services.topic_generator import generate_topics
from app.services.fact_checker import fact_check
from app.services.history_logger import log_conversation

router = APIRouter()

# 1. Standalone Theme Extraction
@router.post("/analyze-event")
def analyze_event(data: EventInput):
    themes = extract_event_themes(data.description)
    return {"topics": themes}

# 2. Fact Check Wrapper
@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check_endpoint(data: FactCheckRequest):
    summary = fact_check(data.query)
    return FactCheckResponse(summary=summary)

# 3. Main Orchestration Route (Extract -> Generate -> Log -> Return)
@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation_endpoint(data: ConversationRequest):
    # Step A: Event analyzer se themes nikalna
    themes = extract_event_themes(data.description)
    
    # Step B: Themes aur interests use karke topics generate karna
    suggestions = generate_topics(themes, data.interests)
    
    # Step C: Automatic side-effect logging (History mein save karna)
    history_data = {
        "event_description": data.description,
        "user_interests": data.interests,
        "extracted_themes": themes,
        "generated_suggestions": suggestions
    }
    log_conversation(history_data)
    
    # Step D: Single structured response return karna
    return ConversationResponse(topics=themes, suggestions=suggestions)