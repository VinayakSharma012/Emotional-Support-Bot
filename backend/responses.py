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

def get_context_aware_response(msg, emotion=None):
    return None

