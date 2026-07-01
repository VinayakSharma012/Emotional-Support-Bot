CRISIS_KEYWORDS = ["suicide", "suicidal", "kill myself", "end my life", "want to die", "feel like dying", "dying today", "i want to die", "i'm going to die", "self harm", "self-harm", "self injury", "cut myself", "hurt myself", "cut my", "hurt my", "overdose", "overdosing", "end it all", "take my own life", "no reason to live", "no point in living", "hopeless", "hopelessness", "worthless", "can't go on", "i can't go on", "can't take it", "give up on life", "not worth living", "not worth it", "want to hurt", "want to harm", "want to injure"]

CRISIS_RESPONSE = {"is_crisis": True, "reply": "I'm really concerned about what you've shared.\n\nPlease reach out for immediate support:\n\niCall (India): 9152987821\nVandrevala Foundation: 1860-2662-345\nAASRA: 9820466726\n\nThese are free, confidential, and available 24/7.\n\nYou are not alone. Your life has value.\nA counselor can help you through this. Please reach out to them or a helpline right now."}


def safety_check(message):
    return CRISIS_RESPONSE if any(kw in message.lower().strip() for kw in CRISIS_KEYWORDS) else {"is_crisis": False, "reply": None}
