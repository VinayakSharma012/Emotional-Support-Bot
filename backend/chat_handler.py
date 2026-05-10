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
    ai_response = get_ai_response(user_message, emotion, history)
    
    if ai_response:
        crisis_intent = detect_crisis_intent(user_message)
        if crisis_intent:
            from backend.safety import CRISIS_RESPONSE
            return {"reply": CRISIS_RESPONSE["reply"], "emotion": "distressed", "is_crisis": True}
        reply = sanitize_reply(ai_response)
        return {"reply": reply, "emotion": emotion, "is_crisis": False}
    
    safety = safety_check(user_message)
    if safety["is_crisis"]:
        return {"reply": safety["reply"], "emotion": "distressed", "is_crisis": True}
    
    reply = get_context_aware_response(user_message, emotion) or get_fallback_response(emotion)
    reply = sanitize_reply(reply)
    return {"reply": reply, "emotion": emotion, "is_crisis": False}

def get_ai_response(msg, emotion, hist=None):
    if not HUGGINGFACE_API_KEY:
        return None
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": _build_prompt(msg, emotion, hist or []),
            "parameters": {"max_new_tokens": 120, "temperature": 0.7, "top_p": 0.9, "return_full_text": False, "do_sample": True},
            "options": {"wait_for_model": True}
        }
        res = requests.post(HF_URL, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        result = res.json()
        return _clean_reply(result[0]["generated_text"]) if result and isinstance(result, list) else None
    except Exception:
        return None

def _build_prompt(msg, emotion, hist):
    conv = "\n".join([f"{'User' if i['role']=='user' else 'Assistant'}: {i['content']}" for i in hist[-8:]]) or "No previous messages."
    return f"""<|system|>
You are a compassionate emotional support chatbot. Your job is to:
1. Listen and validate the user's feelings
2. Show genuine understanding and empathy
3. Ask clarifying questions to understand better
4. Give practical, actionable advice when relevant
5. Keep responses warm, conversational, and under 80 words
6. Never pretend to be a therapist or doctor
7. If user mentions crisis/harm, encourage professional help

Context: User's detected emotion is {emotion}

Recent conversation:
{conv}

Respond naturally, empathetically, and conversationally to the user's message.
<|user|>
{msg}
<|assistant|>"""

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

