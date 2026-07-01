from config.config import FORBIDDEN_FRAGMENTS
from backend.responses import get_fallback_response


def sanitize_reply(text):
    if not text or not text.strip():
        return get_fallback_response("neutral")

    if any(frag in text.lower() for frag in FORBIDDEN_FRAGMENTS):
        return get_fallback_response("negative")

    stripped = text.strip()
    return stripped if stripped[-1] in ".?!" else stripped + "."
