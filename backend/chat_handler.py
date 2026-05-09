import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.safety import safety_check
from backend.emotion import detect_emotion
from backend.responses import get_fallback_response, get_context_aware_response
from backend.sanitizer import sanitize_reply
from config.config import HUGGINGFACE_MODEL

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"


def process_message(user_message, history=None):
    history = history or []

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
    
    # Step 3: Use Hugging Face with recent context, then safe fallbacks.
    reply = get_ai_response(user_message, emotion, history)
    if not reply:
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


def get_ai_response(message, emotion, history=None):
    if not HUGGINGFACE_API_KEY:
        return None

    try:
        prompt = build_support_prompt(message, emotion, history or [])
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 120,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False,
                "do_sample": True,
            },
            "options": {
                "wait_for_model": True,
            },
        }

        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            ai_text = result[0].get("generated_text", "").strip()
            ai_text = clean_ai_reply(ai_text)
            if ai_text:
                return ai_text

        return None

    except Exception as e:
        return None


def build_support_prompt(message, emotion, history):
    conversation_lines = []
    for item in history[-8:]:
        role = "User" if item["role"] == "user" else "Assistant"
        conversation_lines.append(f"{role}: {item['content']}")

    conversation = "\n".join(conversation_lines) if conversation_lines else "No previous messages."

    return (
        "<|system|>\n"
        "You are MindBot, a warm emotional-support chatbot for students. "
        "Use the conversation history so your reply feels contextual and not repetitive. "
        "Validate feelings, ask one gentle follow-up question, and keep replies under 70 words. "
        "Do not diagnose, prescribe, give medical instructions, or pretend to be a therapist. "
        "For crisis or self-harm risk, encourage immediate human help and crisis helplines.\n"
        "<|user|>\n"
        f"Detected emotion: {emotion}\n"
        f"Recent conversation:\n{conversation}\n"
        f"Latest user message: {message}\n"
        "<|assistant|>\n"
    )


def clean_ai_reply(text):
    if not text:
        return ""

    stop_markers = ["<|user|>", "<|system|>", "User:", "Assistant:", "\n\n"]
    cleaned = text.strip()
    for marker in stop_markers:
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()

    return cleaned.strip("\"' ")
