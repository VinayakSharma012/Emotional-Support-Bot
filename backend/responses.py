import random

RESPONSES = {
    "positive": [
        "That's wonderful to hear. What's been making you feel this way? I'm here if you want to share.",
        "I'm so glad you're in a good place! That's something to celebrate. Would you like to tell me more?",
        "That's amazing! It's great to see positivity. Remember, speaking to a counselor can also help sustain this.",
        "Your positive energy is beautiful. What's been bringing you joy? I'm here to listen.",
    ],
    "neutral": [
        "I hear you. Life has its ups and downs. What's on your mind? Would you like to talk about it?",
        "Thanks for opening up. I'm here to listen without judgment. What would help you feel better?",
        "It sounds like you're navigating through things. That takes courage. Would you like to share more?",
        "I'm listening. Sometimes we just need someone to talk to. What's been happening lately?",
    ],
    "negative": [
        "I'm sorry you're going through a tough time. That must be difficult. You're not alone in this. Would you like to talk?",
        "It sounds like things have been rough. Your feelings are completely valid. I'm here for you. Tell me more?",
        "I can hear the struggle in what you're saying. That's okay. You deserve support and I'm here. What's hurting?",
        "That sounds painful. But I want you to know you don't have to carry this alone. I'm listening. Tell me more?",
        "I hear you. Difficult emotions are part of being human. Remember, speaking to a counselor can really help.",
    ],
    "distressed": [
        "I'm genuinely concerned about what you're going through. Please know you're not alone and help is available. Tell me more?",
        "That sounds incredibly overwhelming and painful. You deserve real support. Please consider calling iCall: 9152987821.",
        "I hear so much pain in what you've shared. Your feelings matter deeply. Would you like to talk more or need help?",
        "I can sense you're really struggling. That's real, and you deserve care. A counselor can provide the support you need.",
        "What you're experiencing sounds intensely difficult. Remember, you matter. Help is available: iCall 9152987821.",
    ],
}

def get_fallback_response(emotion):
    emotion = emotion.lower() if emotion else "neutral"
    response_list = RESPONSES.get(emotion, RESPONSES["neutral"])
    return random.choice(response_list)
