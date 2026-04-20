from flask import Blueprint, render_template

clinics_ui_bp = Blueprint("clinics_ui", __name__)


@clinics_ui_bp.route("/", methods=["GET"])
def clinics_home():
    """Placeholder UI page for Clinics search."""
    return render_template("clinics.html")

