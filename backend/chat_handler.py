# ============================================================
# Message Processing: Emotion Detection → AI Response → Crisis Detection
# ============================================================

import os
import sys
import requests
from backend.safety import safety_check, CRISIS_RESPONSE
from backend.emotion import detect_emotion
from backend.responses import get_fallback_response
from backend.sanitizer import sanitize_reply
from config.config import GOOGLE_API_KEY

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def process_message(user_message, history=None):
    # Main function: processes user message and returns bot response
    # 1. Detect user's emotion (positive/negative/neutral/distressed)
    emotion = detect_emotion(user_message)
    # 2. Try to get AI response from Gemini API
    ai_response = get_ai_response(user_message, emotion, history or [])
    
    if ai_response:
        # If we got AI response, check if it's a crisis situation
        if detect_crisis_intent(user_message):
            return {"reply": CRISIS_RESPONSE["reply"], "emotion": "distressed", "is_crisis": True}
        # Return AI response with sanitization
        print(f"[AI] Using Gemini response")
        return {"reply": sanitize_reply(ai_response), "emotion": emotion, "is_crisis": False}
    
    # If AI fails, check for crisis keywords
    safety = safety_check(user_message)
    if safety["is_crisis"]:
        return {"reply": safety["reply"], "emotion": "distressed", "is_crisis": True}
    
    # If everything is ok, return a generic supportive fallback response
    print(f"[FALLBACK] Gemini didn't respond, using fallback")
    return {"reply": sanitize_reply(get_fallback_response(emotion)), "emotion": emotion, "is_crisis": False}

def get_ai_response(msg, emotion, hist):
    # Call Google Gemini API to get intelligent AI response
    # Skip if API key is not configured
    if not GOOGLE_API_KEY:
        return None
    try:
        # Send message to Gemini API with context
        res = requests.post(
            f"{GEMINI_URL}?key={GOOGLE_API_KEY}",
            json={"contents": [{"parts": [{"text": _build_prompt(msg, emotion, hist)}]}]},
            timeout=60
        )
        res.raise_for_status()
        result = res.json()
        # Extract AI response from API result
        if "candidates" in result and result["candidates"]:
            text = result["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return _clean_reply(text) if text else None
        return None
    except:
        # If API fails, return None (will use fallback)
        return None

def _build_prompt(msg, emotion, hist):
    # Build the prompt for AI to generate empathetic response
    # Include recent conversation history to maintain context
    conv = "\n".join([f"{'User' if i['role']=='user' else 'Bot'}: {i['content']}" for i in hist[-4:]]) or "Start of conversation"
    return f"""You are a compassionate support chatbot. Respond warmly and empathetically.
- Validate their feelings
- Ask one helpful follow-up question
- Keep response under 60 words
- Never diagnose or prescribe
- For crisis, encourage professional help

Detected emotion: {emotion}
Recent chat: {conv}
User: {msg}
Bot:"""

def _clean_reply(text):
    # Remove unwanted markers and extra whitespace from AI response
    cleaned = text.strip() if text else ""
    for marker in ["<|user|>", "<|system|>", "User:", "Assistant:", "\n\n"]:
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned.strip("\"' ")

def detect_crisis_intent(msg):
    # Use AI to detect if user is expressing intent to harm themselves
    if not GOOGLE_API_KEY:
        return False
    try:
        # Ask Gemini API to analyze if this is a crisis message
        res = requests.post(
            f"{GEMINI_URL}?key={GOOGLE_API_KEY}",
            json={"contents": [{"parts": [{"text": f"Is the person expressing intent to harm themselves or commit suicide? Message: '{msg}'\n\nAnswer only 'yes' or 'no'."}]}]},
            timeout=45
        )
        res.raise_for_status()
        result = res.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").lower()
        return "yes" in text
    except:
        # If detection fails, assume it's safe
        return False

