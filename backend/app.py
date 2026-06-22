# ============================================================
# Flask Backend Server for Emotional Support Chatbot
# ============================================================

import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import ALLOWED_ORIGINS, FLASK_DEBUG, FLASK_PORT, MAX_HISTORY_MESSAGES, ERROR_MISSING_MESSAGE_FIELD, ERROR_EMPTY_MESSAGE, ERROR_GENERIC
from backend.chat_handler import process_message

# Setup Flask app and allow requests from frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app, resources={r"/chat": {"origins": ALLOWED_ORIGINS}, r"/health": {"origins": ALLOWED_ORIGINS}})

def _now():
    # Get current time in HH:MM format
    return datetime.now().strftime("%H:%M")

def _clean_history(hist):
    # Clean up conversation history: only keep last 8 messages, remove invalid ones
    if not isinstance(hist, list):
        return []
    return [{"role": i.get("role"), "content": i.get("content")[:500]} for i in hist[-MAX_HISTORY_MESSAGES:] 
            if isinstance(i, dict) and i.get("role") in {"user", "bot"} and isinstance(i.get("content"), str) and i.get("content", "").strip()]

@app.route("/")
def serve_index():
    # Serve the main HTML page when user opens the website
    return send_from_directory(frontend_path, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    # Serve CSS, JS, and other static files
    return send_from_directory(frontend_path, filename)

@app.route("/health", methods=["GET"])
def health():
    # Health check endpoint - returns 'ok' if server is running
    return jsonify({"status": "ok"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    # Main chat endpoint - receives user message and returns bot response
    try:
        data = request.get_json() or {}
        msg = (data.get("message") or "").strip()
        # Check if message is valid
        if not msg:
            return jsonify({"error": ERROR_MISSING_MESSAGE_FIELD if "message" not in data else ERROR_EMPTY_MESSAGE}), 400
        # Process message and get bot response
        result = process_message(msg, _clean_history(data.get("history", [])))
        # Return response with timestamp
        return jsonify({**result, "timestamp": _now()}), 200
    except Exception:
        return jsonify({"error": ERROR_GENERIC}), 500

if __name__ == "__main__":
    # On deploy services (like Render) provide a PORT environment variable.
    # Prefer that when available, otherwise fall back to FLASK_PORT from config
    port = int(os.getenv("PORT") or FLASK_PORT)

    # Show whether the Gemini key is configured (without printing the key)
    gemini_present = bool(os.getenv("GOOGLE_API_KEY"))
    print(f"Starting Emotional Support Bot on 0.0.0.0:{port} | Gemini key set: {gemini_present}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=FLASK_DEBUG
    )

