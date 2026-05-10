# ============================================================
# Response Sanitization: Validates and cleans AI responses
# ============================================================

import os
import sys
from config.config import FORBIDDEN_FRAGMENTS
from backend.responses import get_fallback_response

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sanitize_reply(text):
    # Check if response is empty - use fallback if so
    if not text or not text.strip():
        return get_fallback_response("neutral")
    
    # Check if response contains forbidden words (medical advice, diagnosis, etc)
    lowered = text.lower()
    if any(frag in lowered for frag in FORBIDDEN_FRAGMENTS):
        return get_fallback_response("negative")
    
    # Ensure response ends with punctuation
    stripped = text.strip()
    return stripped if stripped[-1] in ".?!" else stripped + "."

