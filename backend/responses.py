import random

RESPONSES = {
    "positive": [
        "That's wonderful to hear! 😊 What's been making you feel this way? I'm here if you want to share.",
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

CONTEXT_RESPONSES = {
    "stress": [
        "Stress can be overwhelming, especially when it affects your grades or future. That's a real concern. Many people struggle with this. Have you talked to someone at school or a counselor about it?",
        "It sounds like academic pressure is weighing on you. That's really common, but it doesn't define your worth. Would you like to talk about what's making it so hard?",
        "Grades can feel like everything, but they don't define your value as a person. If you're struggling, reaching out to a mentor or counselor can really help.",
    ],
    "giving_up": [
        "It sounds like you're feeling defeated right now. That feeling is temporary, even though it doesn't feel that way. Have you talked to anyone about how you're feeling?",
        "When we feel like giving up, that's often a sign we need support. You don't have to go through this alone. Would you like to talk about what's making you want to give up?",
        "I hear hopelessness in what you're saying. That's a signal to reach out for help. Talking to a counselor or trusted adult can make a real difference.",
    ],
    "anxiety": [
        "Anxiety can feel paralyzing. It's important to know that what you're feeling is real, and there are ways to manage it. Have you tried talking to someone about your anxiety?",
        "Feeling anxious is your mind's way of trying to protect you, but sometimes it goes into overdrive. A counselor can teach you techniques to calm that response.",
        "Anxiety is common, and you're not alone in feeling this way. With proper support and strategies, it can get better. Would you like to explore what's triggering it?",
    ],
    "social": [
        "That sounds really hurtful. The way people treat us can deeply affect how we feel about ourselves. Know that their treatment says more about them than about you. Would you like to talk about what happened?",
        "It's painful when you feel disrespected or mistreated by others. Your worth doesn't depend on how they treat you. A counselor can help you process this and build your confidence. Would you like to share more?",
        "Being treated poorly is genuinely hurtful, and your feelings are valid. You deserve respect and kindness. Have you talked to someone you trust about how this is affecting you?",
        "When people treat us badly, it can make us question our own value. But that's not true - you matter. Talking to a counselor or mentor can really help you work through this.",
    ],
    "relationships": [
        "Relationship struggles can be really painful. It sounds like you're hurting. Would you like to talk about what's going on and how it's affecting you?",
        "Conflict with others is tough, and it's natural to feel hurt or frustrated. A counselor can help you navigate these feelings and relationships. Would you like to share more?",
        "When people we care about hurt us, it can feel really isolating. You're not alone in feeling this way. Talking it through with someone can really help.",
    ],
}


def get_context_aware_response(message, emotion):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["grade", "exam", "test", "school", "pressure", "failing", "homework"]):
        return random.choice(CONTEXT_RESPONSES["stress"])
    
    if any(word in message_lower for word in ["giving up", "give up", "no point", "pointless"]):
        return random.choice(CONTEXT_RESPONSES["giving_up"])
    
    if any(word in message_lower for word in ["anxious", "anxiety", "nervous", "worried", "panic"]):
        return random.choice(CONTEXT_RESPONSES["anxiety"])
    
    if any(word in message_lower for word in ["treat me like", "treats me like", "treated badly", "disrespect", "disrespectful", "rude", "mean to me", "everyone hates"]):
        return random.choice(CONTEXT_RESPONSES["social"])
    
    if any(word in message_lower for word in ["relationship", "boyfriend", "girlfriend", "friend", "family", "parents", "argue", "fight", "conflict"]):
        return random.choice(CONTEXT_RESPONSES["relationships"])
    
    return None


def get_fallback_response(emotion):
    emotion = emotion.lower() if emotion else "neutral"
    response_list = RESPONSES.get(emotion, RESPONSES["neutral"])
    return random.choice(response_list)
