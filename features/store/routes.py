from flask import Blueprint, render_template

store_bp = Blueprint("store", __name__)


@store_bp.route("/", methods=["GET"])
def store_home():
    """Placeholder UI page for the Aarohi AI store."""
    return render_template("store.html")

