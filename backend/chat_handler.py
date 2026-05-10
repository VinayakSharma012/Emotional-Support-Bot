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
    emotion = detect_emotion(user_message)
    ai_response = get_ai_response(user_message, emotion, history or [])
    
    if ai_response:
        if detect_crisis_intent(user_message):
            return {"reply": CRISIS_RESPONSE["reply"], "emotion": "distressed", "is_crisis": True}
        return {"reply": sanitize_reply(ai_response), "emotion": emotion, "is_crisis": False}
    
    safety = safety_check(user_message)
    if safety["is_crisis"]:
        return {"reply": safety["reply"], "emotion": "distressed", "is_crisis": True}
    
    return {"reply": sanitize_reply(get_fallback_response(emotion)), "emotion": emotion, "is_crisis": False}

def get_ai_response(msg, emotion, hist):
    if not GOOGLE_API_KEY:
        return None
    try:
        res = requests.post(
            f"{GEMINI_URL}?key={GOOGLE_API_KEY}",
            json={"contents": [{"parts": [{"text": _build_prompt(msg, emotion, hist)}]}]},
            timeout=30
        )
        res.raise_for_status()
        result = res.json()
        if "candidates" in result and result["candidates"]:
            text = result["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return _clean_reply(text) if text else None
        return None
    except:
        return None

def _build_prompt(msg, emotion, hist):
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
    cleaned = text.strip() if text else ""
    for marker in ["<|user|>", "<|system|>", "User:", "Assistant:", "\n\n"]:
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned.strip("\"' ")

def detect_crisis_intent(msg):
    if not GOOGLE_API_KEY:
        return False
    try:
        res = requests.post(
            f"{GEMINI_URL}?key={GOOGLE_API_KEY}",
            json={"contents": [{"parts": [{"text": f"Is the person expressing intent to harm themselves or commit suicide? Message: '{msg}'\n\nAnswer only 'yes' or 'no'."}]}]},
            timeout=15
        )
        res.raise_for_status()
        result = res.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").lower()
        return "yes" in text
    except:
        return False

