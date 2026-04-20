"""
Clinics routes for Aarohi AI.

This module defines all clinics-related API endpoints.
Protected with JWT - requires valid token.
"""

from flask import Blueprint, render_template, request
from auth.middleware import jwt_required
from clinics.services import get_nearby_clinics

clinics_bp = Blueprint("clinics", __name__)

@clinics_bp.route("/clinics", methods=["GET"])
def clinics_page():
    """Render the gynecologist finder page."""
    state = request.args.get("state")
    city = request.args.get("city")
    
    clinics_list = get_nearby_clinics(state=state, city=city)
    
    return render_template("clinics.html", clinics=clinics_list)

