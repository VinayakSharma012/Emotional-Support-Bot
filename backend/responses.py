import random
import re

RESPONSES = {
    "positive": ["That's wonderful! What's been making you feel this way?", "I'm so glad you're in a good place! That's something to celebrate.", "That's amazing! It's great to see positivity.", "Your positive energy is beautiful. What's been bringing you joy?"],
    "neutral": ["I hear you. What's on your mind?", "Thanks for sharing. Tell me more about how you're feeling?", "It sounds like you're working through something. I'm here to listen.", "I'm listening. Sometimes we just need to talk it out."],
    "negative": ["I'm sorry things feel tough right now. You're not alone—I'm here. Tell me more?", "That sounds difficult. Your feelings are valid. What's weighing on you?", "I can hear the struggle. You deserve support. Share what's on your mind?", "That sounds painful. You don't have to carry this alone. I'm here."],
    "distressed": ["I'm genuinely concerned about what you've shared. Please reach out for support. Tell me more?", "That sounds overwhelming and scary. You deserve care and help. What's happening?", "I hear so much pain in what you've shared. You matter and you're not alone.", "I can sense you're really struggling. Professional support can help. Want to talk?"]
}


GROUNDING_RESPONSE = """Here are four grounding techniques you can try right now:

1. 5-4-3-2-1: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, and 1 you taste.
2. Slow breathing: Breathe in for 4, hold for 2, and out for 6. Repeat five times.
3. Feet on the floor: Press both feet down and notice the support, pressure, and temperature for 30 seconds.
4. Cold sensation: Hold something cool or splash cool water on your face, focusing only on the sensation.

Start with whichever feels easiest. Are you somewhere physically safe right now?"""

ACKNOWLEDGEMENT_WORDS = {
    "no",
    "nope",
    "nah",
    "na",
    "yes",
    "yea",
    "yeah",
    "yep",
    "yup",
    "ok",
    "okay",
    "sure",
    "hmm",
    "hm",
}

NEGATIVE_ACKNOWLEDGEMENTS = {"no", "nope", "nah", "na"}


def _normalize_short_message(message):
    return re.sub(r"[^a-z0-9\s']", "", (message or "").lower()).strip()


def _last_bot_message(history):
    for item in reversed(history or []):
        if item.get("role") != "user":
            return item.get("content", "").lower()
    return ""


def get_context_aware_response(message, history=None):
    normalized = _normalize_short_message(message)
    compact = normalized.replace(" ", "")

    if any(term in normalized for term in ("grounding", "ground myself", "ground me")) or compact in {"54321", "5-4-3-2-1"}:
        return GROUNDING_RESPONSE

    if normalized in ACKNOWLEDGEMENT_WORDS:
        last_bot_message = _last_bot_message(history)
        if "music" in last_bot_message or "calm your mind" in last_bot_message:
            if normalized in NEGATIVE_ACKNOWLEDGEMENTS:
                return "Got it. If music isn't helping right now, try a quieter reset: put both feet on the floor and take five slow breaths. What feels strongest right now?"
            return "Got it. If music helps even a little, try one calming song and take slow breaths with it. Is the stress feeling lighter now?"

        return "Got it. I'm here with you. What's feeling most present for you right now?"

    return None


def get_fallback_response(emotion):
    emotion = (emotion or "neutral").lower()
    return random.choice(RESPONSES.get(emotion, RESPONSES["neutral"]))
