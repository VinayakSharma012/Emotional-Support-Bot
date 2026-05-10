# ============================================================
# Fallback Responses: Generic supportive messages by emotion
# ============================================================

import random

# Predefined responses for when AI doesn't respond (fallback)
# Organized by emotion: positive, neutral, negative, distressed
RESPONSES = {
    "positive": ["That's wonderful! What's been making you feel this way?", "I'm so glad you're in a good place! That's something to celebrate.", "That's amazing! It's great to see positivity.", "Your positive energy is beautiful. What's been bringing you joy?"],
    "neutral": ["I hear you. What's on your mind?", "Thanks for sharing. Tell me more about how you're feeling?", "It sounds like you're working through something. I'm here to listen.", "I'm listening. Sometimes we just need to talk it out."],
    "negative": ["I'm sorry things feel tough right now. You're not alone—I'm here. Tell me more?", "That sounds difficult. Your feelings are valid. What's weighing on you?", "I can hear the struggle. You deserve support. Share what's on your mind?", "That sounds painful. You don't have to carry this alone. I'm here."],
    "distressed": ["I'm genuinely concerned about what you've shared. Please reach out for support. Tell me more?", "That sounds overwhelming and scary. You deserve care and help. What's happening?", "I hear so much pain in what you've shared. You matter and you're not alone.", "I can sense you're really struggling. Professional support can help. Want to talk?"]
}

def get_fallback_response(emotion):
    # Return a random supportive message based on detected emotion
    emotion = (emotion or "neutral").lower()
    return random.choice(RESPONSES.get(emotion, RESPONSES["neutral"]))

def get_context_aware_response(msg, emotion=None):
    # Placeholder for future context-aware responses
    return None

