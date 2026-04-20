"""
JWT authentication middleware for Aarohi AI.

Provides jwt_required decorator to protect routes.
Extracts token from Authorization header, decodes with JWT_SECRET_KEY,
and attaches user_id to Flask g.
"""

import jwt
from functools import wraps
from flask import request, g, jsonify
from flask import current_app


def jwt_required(f):
    """
    Decorator that requires a valid JWT in the Authorization header.
    Extracts token, decodes it, sets g.user_id.
    Returns 401 if token is missing or invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1].strip()
        if not token:
            return jsonify({"error": "Token is required"}), 401

        try:
            secret = current_app.config.get("JWT_SECRET_KEY")
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            g.user_id = payload.get("user_id")
            if not g.user_id:
                return jsonify({"error": "Invalid token payload"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
