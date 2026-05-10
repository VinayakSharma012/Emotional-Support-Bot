import sys
import os
import requests
from backend.safety import safety_check
from backend.emotion import detect_emotion
from backend.responses import get_fallback_response, get_context_aware_response
from backend.sanitizer import sanitize_reply
from config.config import HUGGINGFACE_MODEL

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
HF_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

def process_message(user_message, history=None):
    history = history or []
    
    emotion = detect_emotion(user_message)
    
    # Try AI first with short timeout
    ai_response = get_ai_response(user_message, emotion, history)
    
    if ai_response:
        # Check crisis intent if AI responded
        crisis_intent = detect_crisis_intent(user_message)
        if crisis_intent:
            from backend.safety import CRISIS_RESPONSE
            return {"reply": CRISIS_RESPONSE["reply"], "emotion": "distressed", "is_crisis": True}
        reply = sanitize_reply(ai_response)
        return {"reply": reply, "emotion": emotion, "is_crisis": False}
    
    # Fallback to keyword safety check
    safety = safety_check(user_message)
    if safety["is_crisis"]:
        return {"reply": safety["reply"], "emotion": "distressed", "is_crisis": True}
    
    # Use generic fallback
    reply = get_fallback_response(emotion)
    reply = sanitize_reply(reply)
    return {"reply": reply, "emotion": emotion, "is_crisis": False}

def get_ai_response(msg, emotion, hist=None):
    if not HUGGINGFACE_API_KEY:
        return None
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": _build_prompt(msg, emotion, hist or []),
            "parameters": {"max_new_tokens": 100, "temperature": 0.7},
            "options": {"wait_for_model": False}
        }
        res = requests.post(HF_URL, headers=headers, json=payload, timeout=8)
        res.raise_for_status()
        result = res.json()
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            return _clean_reply(result[0]["generated_text"])
        return None
    except requests.exceptions.Timeout:
        return None
    except Exception:
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
    if not text:
        return ""
    cleaned = text.strip()
    for marker in ["<|user|>", "<|system|>", "User:", "Assistant:", "\n\n"]:
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned.strip("\"' ")

def detect_crisis_intent(msg):
    if not HUGGINGFACE_API_KEY:
        return False
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        prompt = f"Is the person expressing intent to harm themselves or commit suicide? Message: '{msg}'\n\nAnswer only 'yes' or 'no'."
        payload = {"inputs": prompt}
        res = requests.post(HF_URL, headers=headers, json=payload, timeout=5)
        res.raise_for_status()
        result = res.json()
        response = result[0]["generated_text"] if result and isinstance(result, list) else ""
        return "yes" in response.lower()
    except Exception:
        return False

