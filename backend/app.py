import sys
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import ALLOWED_ORIGINS, FLASK_DEBUG, FLASK_PORT, MAX_HISTORY_MESSAGES, ERROR_MISSING_MESSAGE_FIELD, ERROR_EMPTY_MESSAGE, ERROR_GENERIC
from backend.chat_handler import process_message

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app, resources={r"/chat": {"origins": ALLOWED_ORIGINS}, r"/health": {"origins": ALLOWED_ORIGINS}})


def get_timestamp():
    return datetime.now().strftime("%H:%M")


def normalize_history(history):
    if not isinstance(history, list):
        return []

    normalized = []
    for item in history[-MAX_HISTORY_MESSAGES:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "bot"} or not isinstance(content, str):
            continue

        content = content.strip()
        if content:
            normalized.append({"role": role, "content": content[:500]})

    return normalized


@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(frontend_path, "index.html")


@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename):
    return send_from_directory(frontend_path, filename)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": ERROR_MISSING_MESSAGE_FIELD}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": ERROR_EMPTY_MESSAGE}), 400

        history = normalize_history(data.get("history", []))

        # Process message through the pipeline
        result = process_message(user_message, history)

        return jsonify({
            "reply": result["reply"],
            "emotion": result["emotion"],
            "is_crisis": result["is_crisis"],
            "timestamp": get_timestamp(),
        }), 200

    except Exception:
        return jsonify({
            "error": ERROR_GENERIC,
            "timestamp": get_timestamp(),
        }), 500


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT)
