import os
from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
FLASK_PORT = 8000

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
GROQ_FALLBACK_MODELS = [
    model.strip()
    for model in os.getenv("GROQ_FALLBACK_MODELS", "llama-3.3-70b-versatile").split(",")
    if model.strip()
]

MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "8"))

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5000,http://localhost:8000,http://127.0.0.1:5000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

FORBIDDEN_FRAGMENTS = [
    "you should take", "you should start", "you should stop", "you must take",
    "take antidepress", "diagnos", "you have", "prescribe", "medication", "ssri",
    "antidepressant", "antipsychotic", "anxiolytic", "tranquilizer", "sedative",
    "prescrib", "drug", "therapy is", "treatment is", "cure for",
]

POLARITY_POSITIVE_THRESHOLD = 0.1      # Above this = positive emotion
POLARITY_NEGATIVE_THRESHOLD = -0.05    # Below this = negative emotion
SUBJECTIVITY_DISTRESS_THRESHOLD = 0.55 # Above this with negative = distressed

ERROR_EMPTY_MESSAGE = "Empty message"
ERROR_MISSING_MESSAGE_FIELD = "Missing 'message' field"
ERROR_GENERIC = "An error occurred. Please try again."
