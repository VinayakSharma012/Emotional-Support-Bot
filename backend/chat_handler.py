import os
import sys
import requests
from backend.safety import safety_check, CRISIS_RESPONSE
from backend.emotion import detect_emotion
from backend.responses import get_fallback_response
from backend.sanitizer import sanitize_reply
from config.config import HUGGINGFACE_MODEL

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
HF_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

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
    if not HUGGINGFACE_API_KEY:
        return None
    try:
        res = requests.post(HF_URL, headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}, 
                          json={"inputs": _build_prompt(msg, emotion, hist), 
                                "parameters": {"max_new_tokens": 100, "temperature": 0.7},
                                "options": {"wait_for_model": True}}, timeout=30)
        res.raise_for_status()
        result = res.json()
        return _clean_reply(result[0]["generated_text"]) if isinstance(result, list) and result and "generated_text" in result[0] else None
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
    if not HUGGINGFACE_API_KEY:
        return False
    try:
        res = requests.post(HF_URL, headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}, 
                          json={"inputs": f"Is the person expressing intent to harm themselves or commit suicide? Message: '{msg}'\n\nAnswer only 'yes' or 'no'."}, timeout=15)
        res.raise_for_status()
        result = res.json()
        return "yes" in (result[0]["generated_text"] if isinstance(result, list) and result else "").lower()
    except:
        return False

