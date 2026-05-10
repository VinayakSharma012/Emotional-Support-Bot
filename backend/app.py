import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config.config import ALLOWED_ORIGINS, FLASK_DEBUG, FLASK_PORT, MAX_HISTORY_MESSAGES, ERROR_MISSING_MESSAGE_FIELD, ERROR_EMPTY_MESSAGE, ERROR_GENERIC
from backend.chat_handler import process_message

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app, resources={r"/chat": {"origins": ALLOWED_ORIGINS}, r"/health": {"origins": ALLOWED_ORIGINS}})

def _now():
    return datetime.now().strftime("%H:%M")

def _clean_history(hist):
    if not isinstance(hist, list):
        return []
    return [{"role": i.get("role"), "content": i.get("content")[:500]} for i in hist[-MAX_HISTORY_MESSAGES:] 
            if isinstance(i, dict) and i.get("role") in {"user", "bot"} and isinstance(i.get("content"), str) and i.get("content", "").strip()]

@app.route("/")
def serve_index():
    return send_from_directory(frontend_path, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(frontend_path, filename)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        msg = (data.get("message") or "").strip()
        if not msg:
            return jsonify({"error": ERROR_MISSING_MESSAGE_FIELD if "message" not in data else ERROR_EMPTY_MESSAGE}), 400
        result = process_message(msg, _clean_history(data.get("history", [])))
        return jsonify({**result, "timestamp": _now()}), 200
    except Exception:
        return jsonify({"error": ERROR_GENERIC}), 500

if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT)

