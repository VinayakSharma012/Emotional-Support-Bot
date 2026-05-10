# ============================================================
# Configuration: Settings for the entire application
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Server Settings
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
FLASK_PORT = 8000

# Google Gemini API Key (get free from https://aistudio.google.com)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Conversation Settings
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "8"))

# CORS Settings: Which websites can access this API
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5000,http://localhost:8000,http://127.0.0.1:5000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

# Words/phrases AI should NOT say (medical advice, prescriptions, diagnoses)
FORBIDDEN_FRAGMENTS = [
    "you should take", "you should start", "you should stop", "you must take",
    "take antidepress", "diagnos", "you have", "prescribe", "medication", "ssri",
    "antidepressant", "antipsychotic", "anxiolytic", "tranquilizer", "sedative",
    "prescrib", "drug", "therapy is", "treatment is", "cure for",
]

# Emotion Detection Thresholds (TextBlob sentiment analysis)
# Polarity: -1 (very negative) to +1 (very positive)
POLARITY_POSITIVE_THRESHOLD = 0.1      # Above this = positive emotion
POLARITY_NEGATIVE_THRESHOLD = -0.05    # Below this = negative emotion
SUBJECTIVITY_DISTRESS_THRESHOLD = 0.55 # Above this with negative = distressed

# Error Messages
ERROR_EMPTY_MESSAGE = "Empty message"
ERROR_MISSING_MESSAGE_FIELD = "Missing 'message' field"
ERROR_GENERIC = "An error occurred. Please try again."
