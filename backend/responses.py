import random

RESPONSES = {
    "positive": ["That's wonderful! What's been making you feel this way?", "I'm so glad you're in a good place! That's something to celebrate.", "That's amazing! It's great to see positivity.", "Your positive energy is beautiful. What's been bringing you joy?"],
    "neutral": ["I hear you. Life has its ups and downs. What's on your mind?", "Thanks for opening up. What would help you feel better?", "It sounds like you're navigating through things. That takes courage.", "I'm listening. Sometimes we just need someone to talk to."],
    "negative": ["I'm sorry you're going through a tough time. You're not alone. Would you like to talk?", "It sounds like things have been rough. Your feelings are valid. Tell me more?", "I can hear the struggle. You deserve support and I'm here. What's hurting?", "That sounds painful. You don't have to carry this alone. Tell me more?"],
    "distressed": ["I'm genuinely concerned about what you're going through. Help is available. Tell me more?", "That sounds overwhelming. You deserve support.", "I hear so much in what you've shared. Your feelings matter deeply.", "I can sense you're really struggling. You deserve care."]
}

def get_fallback_response(emotion):
    emotion = (emotion or "neutral").lower()
    return random.choice(RESPONSES.get(emotion, RESPONSES["neutral"]))

CONTEXT = {
    "crush": ("That sounds uplifting. What felt best about meeting them?", "It's meaningful to notice how people make us feel."),
    "rejection": "I'm sorry you were treated that way. Your worth isn't defined by how others treat you. Would you like to tell me what happened?",
    "anxiety": "Anxiety is your mind's way of protecting you, but it can feel overwhelming. Try: deep breathing (4-count in, 6-count out), grounding (5 senses), or talking it through. What's worrying you?",
    "exam": "Academic pressure is real. Break it into smaller steps, take breaks, and remember: one exam doesn't define you. What specific part feels most overwhelming?",
    "hopeless": "I know things feel dark right now, but these feelings can change. You matter. Please talk to someone—a friend, counselor, or crisis helpline. You're not alone.",
    "stress": "Stress is a signal your body needs care. Try: exercise, sleep, journaling, or talking. What's been building up?",
    "loneliness": "Feeling isolated is painful, but you're not truly alone. Reach out—even a text to one person helps. What's keeping you isolated?",
    "sleep": "Poor sleep worsens everything. Try: consistent bedtime, no screens 30min before, deep breathing, or warm milk. How's your sleep been?"
}

def get_context_aware_response(msg, emotion=None):
    if not msg:
        return None
    text = msg.lower()
    if any(kw in text for kw in ("crush", "met", "date", "liked", "love", "she likes", "he likes")):
        return CONTEXT["crush"][0] if any(w in text for w in ("happy", "glad", "excited")) else CONTEXT["crush"][1]
    if any(kw in text for kw in ("treat me", "treats me", "mean to me", "rude", "insulted", "bully", "picked on", "rejected", "reject")):
        return CONTEXT["rejection"]
    if any(kw in text for kw in ("anxious", "anxiety", "panic", "nervous", "worried", "worrying", "anxious")):
        return CONTEXT["anxiety"]
    if any(kw in text for kw in ("exam", "test", "grade", "homework", "fail", "pressure", "study", "assignment")):
        return CONTEXT["exam"]
    if any(kw in text for kw in ("give up", "no point", "hopeless", "can't go on", "done", "worthless")):
        return CONTEXT["hopeless"]
    if any(kw in text for kw in ("stress", "stressed", "overwhelmed", "too much", "pressure")):
        return CONTEXT["stress"]
    if any(kw in text for kw in ("lonely", "alone", "isolated", "no one", "nobody", "by myself")):
        return CONTEXT["loneliness"]
    if any(kw in text for kw in ("sleep", "can't sleep", "insomnia", "tired", "exhausted", "sleepy")):
        return CONTEXT["sleep"]
    return None

