import sys
import os
from textblob import TextBlob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    POLARITY_POSITIVE_THRESHOLD,
    POLARITY_NEGATIVE_THRESHOLD,
    SUBJECTIVITY_DISTRESS_THRESHOLD,
)


def detect_emotion(message):
    try:
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Distressed: high emotional intensity + negative sentiment
        if subjectivity > SUBJECTIVITY_DISTRESS_THRESHOLD and polarity < 0:
            return "distressed"
        
        # Positive: clearly positive sentiment
        if polarity > POLARITY_POSITIVE_THRESHOLD:
            return "positive"
        
        # Negative: clearly negative sentiment
        elif polarity < POLARITY_NEGATIVE_THRESHOLD:
            return "negative"
        
        # Neutral: everything else
        else:
            return "neutral"
    
    except Exception as e:
        return "neutral"
