import requests
from backend.safety import safety_check, CRISIS_RESPONSE
from backend.emotion import detect_emotion
from backend.responses import get_context_aware_response, get_fallback_response
from backend.sanitizer import sanitize_reply
from config.config import GROQ_API_KEY, GROQ_FALLBACK_MODELS, GROQ_MODEL

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _groq_models():
    return list(dict.fromkeys([GROQ_MODEL, *GROQ_FALLBACK_MODELS]))


def _post_groq(messages, temperature, timeout, model):
    return requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=timeout,
    )


def _log_groq_error(error, model):
    response = getattr(error, "response", None)
    if response is None:
        print(f"[GROQ] {model} request failed: {str(error)[:120]}")
        return

    detail = response.text.strip().replace("\n", " ")[:250]
    print(f"[GROQ] {model} returned {response.status_code}: {detail}")


def _is_auth_or_billing_error(error):
    response = getattr(error, "response", None)
    return response is not None and response.status_code in {401, 403}


def process_message(user_message, history=None):
    history = history or []

    safety = safety_check(user_message)
    if safety["is_crisis"]:
        return {"reply": safety["reply"], "emotion": "distressed", "is_crisis": True}

    emotion = detect_emotion(user_message)

    context_response = get_context_aware_response(user_message, history)
    if context_response:
        return {"reply": sanitize_reply(context_response), "emotion": emotion, "is_crisis": False}

    ai_response = get_ai_response(user_message, emotion, history)

    if ai_response:
        if detect_crisis_intent(user_message):
            return {"reply": CRISIS_RESPONSE["reply"], "emotion": "distressed", "is_crisis": True}
        print(f"[AI] Using Groq response")
        return {"reply": sanitize_reply(ai_response), "emotion": emotion, "is_crisis": False}

    print(f"[FALLBACK] Groq didn't respond, using fallback")
    return {"reply": sanitize_reply(get_fallback_response(emotion)), "emotion": emotion, "is_crisis": False}


def get_ai_response(msg, emotion, hist):
    if not GROQ_API_KEY:
        return None

    messages = [
        {
            "role": "system",
            "content": "You are a compassionate support chatbot. Never diagnose or prescribe.",
        },
        {"role": "user", "content": _build_prompt(msg, emotion, hist)},
    ]

    for model in _groq_models():
        for attempt in range(2):
            try:
                res = _post_groq(messages, temperature=0.7, timeout=90, model=model)
                res.raise_for_status()
                result = res.json()
                text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                if text:
                    return _clean_reply(text)
            except Exception as e:
                _log_groq_error(e, model)
                if _is_auth_or_billing_error(e):
                    return None
                if attempt == 0:
                    print(f"[RETRY] Retrying Groq model {model}...")

    return None


def _build_prompt(msg, emotion, hist):
    conv = "\n".join([f"{'User' if i['role']=='user' else 'Bot'}: {i['content']}" for i in hist[-4:]]) or "Start of conversation"
    return f"""You are a compassionate support chatbot. Respond warmly and empathetically.
- Validate their feelings
- First answer the user's explicit question or request with practical, relevant information
- Then ask at most one helpful follow-up question
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
    if not GROQ_API_KEY:
        return False
    try:
        res = _post_groq(
            [
                {"role": "system", "content": "Answer only yes or no."},
                {
                    "role": "user",
                    "content": f"Is the person expressing intent to harm themselves or commit suicide? Message: '{msg}'",
                },
            ],
            temperature=0,
            timeout=45,
            model=_groq_models()[0],
        )
        res.raise_for_status()
        result = res.json()
        text = result.get("choices", [{}])[0].get("message", {}).get("content", "").lower()
        return "yes" in text
    except Exception:
        return False
