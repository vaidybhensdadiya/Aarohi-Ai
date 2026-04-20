"""
Schemes routes for Aarohi AI.

This module defines:
- API endpoints for schemes (under /api/schemes)
- UI endpoint for the Schemes page (under /schemes)
"""

from flask import Blueprint, jsonify, render_template, request

from auth.middleware import jwt_required
from .services import get_eligible_schemes, get_states

schemes_bp = Blueprint("schemes", __name__)


@schemes_bp.route("/api/schemes", methods=["GET"])
@jwt_required
def schemes_index():
    """Simple placeholder JSON API for schemes (kept for future use)."""
    return jsonify({"message": "Schemes API - coming soon"}), 200


@schemes_bp.route("/schemes", methods=["GET"])
def schemes_page():
    """
    Render the Schemes page with eligibility filters.

    Query params:
        - age   (required for eligibility)
        - state (optional)
    """
    age_raw = (request.args.get("age") or "").strip()
    state = (request.args.get("state") or "").strip()

    eligible_schemes = []
    error = None

    if age_raw:
        try:
            age = int(age_raw)
            if age < 0 or age > 120:
                error = "Please enter a realistic age."
            else:
                eligible_schemes = get_eligible_schemes(age, state or None)
        except ValueError:
            error = "Please enter a valid age."
    else:
        # Age is required to compute eligibility
        error = "Please enter your age to see eligible schemes."

    states = get_states()

    return render_template(
        "schemes.html",
        schemes=eligible_schemes,
        states=states,
        selected_state=state,
        age=age_raw,
        error=error,
    )
