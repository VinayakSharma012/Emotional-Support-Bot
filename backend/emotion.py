# ============================================================
# Emotion Detection: Analyzes user message sentiment
# ============================================================

import os
import sys
from textblob import TextBlob
from config.config import POLARITY_POSITIVE_THRESHOLD, POLARITY_NEGATIVE_THRESHOLD, SUBJECTIVITY_DISTRESS_THRESHOLD

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def detect_emotion(message):
    # Analyze message sentiment and classify into: positive, negative, neutral, or distressed
    try:
        blob = TextBlob(message)
        pol, subj = blob.sentiment.polarity, blob.sentiment.subjectivity
        # If message is very emotional (high subjectivity) AND negative, mark as distressed
        if subj > SUBJECTIVITY_DISTRESS_THRESHOLD and pol < 0:
            return "distressed"
        # Otherwise classify by polarity (positiveness)
        return "positive" if pol > POLARITY_POSITIVE_THRESHOLD else "negative" if pol < POLARITY_NEGATIVE_THRESHOLD else "neutral"
    except Exception:
        # If analysis fails, default to neutral
        return "neutral"

