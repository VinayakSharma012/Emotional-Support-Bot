import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.safety import safety_check
from backend.emotion import detect_emotion
from backend.responses import get_fallback_response, get_context_aware_response
from backend.sanitizer import sanitize_reply

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"


def process_message(user_message):
    # Step 1: Safety check (highest priority)
    safety_result = safety_check(user_message)
    if safety_result["is_crisis"]:
        return {
            "reply": safety_result["reply"],
            "emotion": "distressed",
            "is_crisis": True,
        }

    # Step 2: Emotion detection
    emotion = detect_emotion(user_message)
    
    # Step 3: Use context-aware response (best quality)
    reply = get_context_aware_response(user_message, emotion)
    if not reply:
        reply = get_fallback_response(emotion)
    
    # Step 4: Sanitize response
    reply = sanitize_reply(reply)

    return {
        "reply": reply,
        "emotion": emotion,
        "is_crisis": False,
    }


def get_ai_response(message, emotion):
    if not HUGGINGFACE_API_KEY:
        return get_fallback_response(emotion)

    try:
        prompt = f"User is feeling {emotion}. They say: '{message}'. Respond supportively:"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "do_sample": True,
            }
        }

        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            ai_text = result[0].get("generated_text", "").strip()
            if prompt in ai_text:
                ai_text = ai_text.replace(prompt, "").strip()
            if ai_text:
                return ai_text

        return get_fallback_response(emotion)

    except Exception as e:
        return get_fallback_response(emotion)
