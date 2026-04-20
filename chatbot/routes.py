"""
Chatbot routes for Aarohi AI.

POST /api/chatbot/chat - Send message, get AI response (JWT required)
"""

from flask import Blueprint, request, jsonify, g
from flask import current_app

from auth.middleware import jwt_required
from chatbot import services

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chat", methods=["POST"])
@jwt_required
def chat():
    """
    POST /api/chatbot/chat
    Input: { "message": "user text" }
    Requires: Authorization: Bearer <token>
    """
    data = request.get_json(silent=True)
    message = data.get("message") if data else None

    if not message or not isinstance(message, str):
        return jsonify({"error": "Message is required"}), 400

    user_id = g.user_id
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "Gemini API not configured"}), 500

    response_text, error = services.process_chat(user_id, message.strip(), api_key)

    if error:
        return jsonify({"error": error}), 500

    return jsonify({"response": response_text}), 200


@chatbot_bp.route("/", methods=["GET"])
@jwt_required
def chatbot_index():
    """Placeholder route for chatbot module."""
    return jsonify({"message": "Chatbot module", "endpoints": {"chat": "POST /api/chatbot/chat"}}), 200
