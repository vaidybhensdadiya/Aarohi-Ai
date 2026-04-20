from flask import Blueprint, render_template

schemes_ui_bp = Blueprint("schemes_ui", __name__)


@schemes_ui_bp.route("/", methods=["GET"])
def schemes_home():
    """Placeholder UI page for Government Schemes."""
    return render_template("schemes.html")

