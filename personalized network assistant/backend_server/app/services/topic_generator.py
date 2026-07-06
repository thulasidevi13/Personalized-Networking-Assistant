# app/services/topic_generator.py

from transformers import pipeline, set_seed
from app.config import MODEL_NAMES

# Reproducibility ke liye random seed fix karna
set_seed(42)

# Module level par GPT-2 pipeline load karna
generator = pipeline("text-generation", model=MODEL_NAMES["topic_generation"])

def generate_topics(themes: list, interests: list) -> list:
    # Themes aur interests ko text mein badalna
    themes_str = ", ".join(themes) if themes else "various topics"
    interests_str = ", ".join(interests) if interests else "learning new things"
    
    # First-person context narrative prompt banana
    prompt = (
        f"I am attending an event focused on {themes_str}. "
        f"My professional interests include {interests_str}. "
        f"Here are some great conversation starters I can use:\n-"
    )
    
    # GPT-2 se text generate karna (max_length=80 tokens)
    output = generator(
        prompt, 
        max_length=80, 
        num_return_sequences=1,
        truncation=True,
        pad_token_id=50256
    )
    
    generated_text = output[0]["generated_text"]
    
    # Prompt wale text ko ignore karke sirf naya AI generated text nikalna
    new_text = generated_text[len(prompt):]
    
    # Post-processing: Newline se split karna
    lines = new_text.split('\n')
    clean_suggestions = []
    
    for line in lines:
        # Bullet markers (-, *) aur spaces clean karna
        clean_line = line.strip().lstrip('-').lstrip('*').strip()
        
        if clean_line:
            clean_suggestions.append(clean_line)
            
        # Sirf pehli 3 lines extract karna
        if len(clean_suggestions) == 3:
            break
            
    return clean_suggestions