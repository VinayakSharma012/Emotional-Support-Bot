CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life",
    "want to die", "feel like dying", "dying today", "i want to die", "i'm going to die",
    "self harm", "self-harm", "self injury", "cut myself", "hurt myself",
    "overdose", "overdosing", "end it all", "take my own life",
    "no reason to live", "no point in living", "hopeless", "hopelessness",
    "worthless", "can't go on", "i can't go on", "can't take it",
    "give up on life", "not worth living", "not worth it",
    "want to hurt", "want to harm", "want to injure",
]

CRISIS_RESPONSE = {
    "is_crisis": True,
    "reply": (
        "I'm really concerned about what you've shared.\n\n"
        "Please reach out for immediate support:\n\n"
        "iCall (India): 9152987821\n"
        "Vandrevala Foundation: 1860-2662-345\n"
        "AASRA: 9820466726\n\n"
        "These are free, confidential, and available 24/7.\n\n"
        "You are not alone. Your life has value.\n"
        "A counselor can help you through this. Please reach out to them or a helpline right now."
    ),
}


def safety_check(message):
    message_lower = message.lower().strip()
    
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return CRISIS_RESPONSE
    
    return {"is_crisis": False, "reply": None}
