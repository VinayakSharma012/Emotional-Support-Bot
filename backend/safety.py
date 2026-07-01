import re


CRISIS_KEYWORDS = [
    "suicide",
    "suicidal",
    "kill myself",
    "end my life",
    "want to die",
    "feel like dying",
    "dying today",
    "i want to die",
    "i'm going to die",
    "i'll die",
    "ill die",
    "i will die",
    "self harm",
    "self-harm",
    "self injury",
    "cut myself",
    "hurt myself",
    "cut my",
    "hurt my",
    "overdose",
    "overdosing",
    "end it all",
    "take my own life",
    "no reason to live",
    "no point in living",
    "hopeless",
    "hopelessness",
    "worthless",
    "can't go on",
    "i can't go on",
    "can't take it",
    "give up on life",
    "not worth living",
    "not worth it",
    "want to hurt",
    "want to harm",
    "want to injure",
]

CRISIS_RESPONSE = {"is_crisis": True, "reply": "I'm really concerned about what you've shared.\n\nPlease reach out for immediate support:\n\niCall (India): 9152987821\nVandrevala Foundation: 1860-2662-345\nAASRA: 9820466726\n\nThese are free, confidential, and available 24/7.\n\nYou are not alone. Your life has value.\nA counselor can help you through this. Please reach out to them or a helpline right now."}


def _normalize(message):
    normalized = (message or "").lower().replace("’", "'")
    normalized = normalized.replace("-", " ")
    normalized = re.sub(r"[^a-z0-9'\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _keyword_pattern(keyword):
    escaped = re.escape(_normalize(keyword)).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")


CRISIS_PATTERNS = [_keyword_pattern(keyword) for keyword in CRISIS_KEYWORDS]


def safety_check(message):
    normalized = _normalize(message)
    if any(pattern.search(normalized) for pattern in CRISIS_PATTERNS):
        return CRISIS_RESPONSE
    return {"is_crisis": False, "reply": None}
