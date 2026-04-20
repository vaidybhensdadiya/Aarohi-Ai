"""
Authentication services for Aarohi AI.

Business logic for user registration, login, password hashing, and JWT token generation.
Uses the `users` table: id, name, email_id, age, password_hash, created_at
"""

from typing import Optional, Tuple

import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection
from flask import current_app


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using werkzeug's secure hashing.
    Uses pbkdf2:sha256 by default.
    """
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify a plain-text password against a stored hash.
    Returns True if password matches, False otherwise.
    """
    return check_password_hash(password_hash, password)


def generate_jwt_token(user_id: int) -> str:
    """
    Generate a JWT token for the given user_id.
    Token expires in 24 hours (from config).
    Payload includes: user_id, exp (expiry), iat (issued at).
    """
    secret = current_app.config.get("JWT_SECRET_KEY")
    hours = current_app.config.get("JWT_EXPIRATION_HOURS", 24)
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=hours),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def get_user_by_email(email_id: str) -> Optional[dict]:
    """
    Fetch a user by email_id from the users table.
    Returns user dict (with password_hash) or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email_id, age, password_hash, created_at FROM users WHERE email_id = %s",
            (email_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    except Exception:
        return None
    finally:
        if conn:
            conn.close()


def register_user(name: str, email_id: str, age: int, password: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Register a new user. Validates inputs, checks email uniqueness, hashes password, inserts.

    Returns:
        (user_dict, None) on success - user_dict has id, name, email_id, age (no password_hash)
        (None, error_message) on failure - error_message suitable for API response
    """
    # Check if email already exists
    existing = get_user_by_email(email_id)
    if existing:
        return None, "Email already exists"

    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        password_hash = hash_password(password)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email_id, age, password_hash) VALUES (%s, %s, %s, %s)",
            (name.strip(), email_id.strip().lower(), age, password_hash),
        )
        user_id = cursor.lastrowid
        cursor.close()

        return {
            "id": user_id,
            "name": name.strip(),
            "email_id": email_id.strip().lower(),
            "age": age,
        }, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()


def authenticate_user(email_id: str, password: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Authenticate user by email_id and password.
    Verifies password hash against stored hash.

    Returns:
        (user_dict, None) on success - user_dict has id, name, email_id, age (no password_hash)
        (None, error_message) on failure
    """
    user = get_user_by_email(email_id)
    if not user:
        return None, "Invalid email or password"

    if not verify_password(user["password_hash"], password):
        return None, "Invalid email or password"

    # Return user info without password_hash
    return {
        "id": user["id"],
        "name": user["name"],
        "email_id": user["email_id"],
        "age": user["age"],
    }, None
