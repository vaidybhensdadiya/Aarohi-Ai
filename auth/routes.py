"""
Authentication routes for Aarohi AI.

API endpoints for user registration and login.
Uses the `users` table: id, name, email_id, age, password_hash, created_at
"""

from flask import Blueprint, request, jsonify, session

from auth import services

auth_bp = Blueprint("auth", __name__)


def _validate_register_input(data: dict) -> tuple[bool, str]:
    """
    Validate register request body.
    Returns (is_valid, error_message).
    """
    if not data:
        return False, "Request body is required"
    name = data.get("name")
    email_id = data.get("email_id")
    age = data.get("age")
    password = data.get("password")

    if not name or not isinstance(name, str) or not name.strip():
        return False, "Name is required and must be a non-empty string"
    if not email_id or not isinstance(email_id, str) or not email_id.strip():
        return False, "Email is required and must be a non-empty string"
    if not isinstance(age, (int, str)):
        return False, "Age is required"
    try:
        age_int = int(age) if isinstance(age, str) else age
    except (ValueError, TypeError):
        return False, "Age must be a valid integer"
    if age_int < 1 or age_int > 150:
        return False, "Age must be between 1 and 150"
    if not password or not isinstance(password, str):
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    return True, ""


def _validate_login_input(data: dict) -> tuple[bool, str]:
    """
    Validate login request body.
    Returns (is_valid, error_message).
    """
    if not data:
        return False, "Request body is required"
    email_id = data.get("email_id")
    password = data.get("password")

    if not email_id or not isinstance(email_id, str) or not email_id.strip():
        return False, "Email is required and must be a non-empty string"
    if not password or not isinstance(password, str):
        return False, "Password is required"

    return True, ""


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/auth/register

    Input JSON: { "name": "", "email_id": "", "age": "", "password": "" }
    - Validates all fields
    - Checks if email_id already exists
    - Hashes password and inserts user
    - Returns success + user id (no password_hash)
    """
    data = request.get_json(silent=True)
    is_valid, err = _validate_register_input(data)
    if not is_valid:
        return jsonify({"error": err}), 400

    name = data["name"].strip()
    email_id = data["email_id"].strip().lower()
    age = int(data["age"]) if isinstance(data["age"], str) else data["age"]
    password = data["password"]

    user, error = services.register_user(name, email_id, age, password)

    if error == "Email already exists":
        return jsonify({"error": "Email already exists"}), 409
    if error == "Database connection failed":
        return jsonify({"error": "Database connection failed"}), 500
    if error:
        return jsonify({"error": "Internal server error"}), 500

    token = services.generate_jwt_token(user["id"])
    token_str = token if isinstance(token, str) else token.decode("utf-8")
    
    # Set session for ecommerce feature
    session["user_id"] = user["id"]

    return (
        jsonify({
            "message": "User registered successfully",
            "token": token_str,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email_id": user["email_id"],
                "age": user["age"],
            },
        }),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/auth/login

    Input JSON: { "email_id": "", "password": "" }
    - Fetches user by email_id
    - Verifies password hash
    - Generates JWT token (24h expiry)
    - Returns token + basic user info
    """
    data = request.get_json(silent=True)
    is_valid, err = _validate_login_input(data)
    if not is_valid:
        return jsonify({"error": err}), 400

    email_id = data["email_id"].strip().lower()
    password = data["password"]

    user, error = services.authenticate_user(email_id, password)

    if error:
        return jsonify({"error": "Invalid email or password"}), 401

    token = services.generate_jwt_token(user["id"])

    # PyJWT 2.x may return str or bytes; ensure string for JSON
    token_str = token if isinstance(token, str) else token.decode("utf-8")
    
    # Set session for ecommerce feature
    session["user_id"] = user["id"]

    return (
        jsonify({
            "message": "Login successful",
            "token": token_str,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email_id": user["email_id"],
                "age": user["age"],
            },
        }),
        200,
    )


@auth_bp.route("/", methods=["GET"])
def auth_index():
    """Placeholder route - auth module info."""
    return jsonify({
        "message": "Auth module",
        "endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
        },
    }), 200
