from textblob import TextBlob
from config.config import POLARITY_POSITIVE_THRESHOLD, POLARITY_NEGATIVE_THRESHOLD, SUBJECTIVITY_DISTRESS_THRESHOLD

def detect_emotion(message):
    try:
        blob = TextBlob(message)
        pol, subj = blob.sentiment.polarity, blob.sentiment.subjectivity
        if subj > SUBJECTIVITY_DISTRESS_THRESHOLD and pol < 0:
            return "distressed"
        return "positive" if pol > POLARITY_POSITIVE_THRESHOLD else "negative" if pol < POLARITY_NEGATIVE_THRESHOLD else "neutral"
    except Exception:
        return "neutral"

