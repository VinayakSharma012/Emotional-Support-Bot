import sys
import os
from config.config import FORBIDDEN_FRAGMENTS
from backend.responses import get_fallback_response

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sanitize_reply(text):
    if not text or not text.strip():
        return get_fallback_response("neutral")
    lowered = text.lower()
    if any(frag in lowered for frag in FORBIDDEN_FRAGMENTS):
        return get_fallback_response("negative")
    stripped = text.strip()
    return stripped if stripped[-1] in ".?!" else stripped + "."

