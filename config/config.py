import os
from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG = True
FLASK_PORT = 8000

FORBIDDEN_FRAGMENTS = [
    "you should take", "you should start", "you should stop", "you must take",
    "take antidepress", "diagnos", "you have", "prescribe", "medication", "ssri",
    "antidepressant", "antipsychotic", "anxiolytic", "tranquilizer", "sedative",
    "prescrib", "drug", "therapy is", "treatment is", "cure for",
]

ALLOWED_REPLY_ENDINGS = [
    "I'm here if you want to talk more.",
    "Would you like to tell me more?",
    "Remember, speaking to a counselor can also help.",
]

POLARITY_POSITIVE_THRESHOLD = 0.1
POLARITY_NEGATIVE_THRESHOLD = -0.05
SUBJECTIVITY_DISTRESS_THRESHOLD = 0.55

ERROR_EMPTY_MESSAGE = "Empty message"
ERROR_MISSING_MESSAGE_FIELD = "Missing 'message' field"
ERROR_GENERIC = "An error occurred. Please try again."
