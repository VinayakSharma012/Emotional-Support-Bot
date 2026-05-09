import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import FORBIDDEN_FRAGMENTS
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
    
    if not stripped.endswith(".") and not stripped.endswith("?") and not stripped.endswith("!"):
        stripped += "."

    return stripped
