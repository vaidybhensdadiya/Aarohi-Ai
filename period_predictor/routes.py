from flask import Blueprint, request, jsonify, session
from auth.middleware import jwt_required

from period_predictor.services import run_prediction

period_predictor_bp = Blueprint("period_predictor", __name__)


@period_predictor_bp.route("/", methods=["GET"])
@jwt_required
def index():
    return jsonify({
        "module": "Period Predictor",
        "status": "ready"
    })


@period_predictor_bp.route("/api/predict-period", methods=["POST"])
@jwt_required
def predict_period():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user_id = session["user_id"]

    result, error = run_prediction(user_id, data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 200
