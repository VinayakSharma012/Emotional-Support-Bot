import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import FORBIDDEN_FRAGMENTS, ALLOWED_REPLY_ENDINGS
from backend.responses import get_fallback_response


def sanitize_reply(text):
    if not text or text.strip() == "":
        return get_fallback_response("neutral")

    lowered = text.lower()

    # Check for forbidden phrases
    for frag in FORBIDDEN_FRAGMENTS:
        if frag in lowered:
            return get_fallback_response("negative")

    stripped = text.strip()
    
    # Ensure response ends with one of the allowed endings
    if not any(stripped.lower().endswith(e) for e in ALLOWED_REPLY_ENDINGS):
        if not stripped.endswith(".") and not stripped.endswith("?"):
            stripped += "."
        stripped = f"{stripped} {ALLOWED_REPLY_ENDINGS[0]}"

    return stripped
