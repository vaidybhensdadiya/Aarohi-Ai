from flask import Flask, jsonify, render_template, redirect, url_for, request, g
from config import Config
import os
import time

from database import get_db_connection
from auth.routes import auth_bp
from auth.middleware import jwt_required
from chatbot.routes import chatbot_bp
from period_predictor.routes import period_predictor_bp
from period_predictor import services as period_services
from schemes.routes import schemes_bp
from ecommerce.routes import ecommerce_bp
from clinics.routes import clinics_bp

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from monitoring.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS_IN_PROGRESS,
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # -----------------------------------
    # DATABASE CONNECTION CHECK
    # -----------------------------------
    conn = get_db_connection()
    if conn:
        print("✅ Database connected successfully")
        conn.close()
    else:
        print("❌ Database connection failed")

    # -----------------------------------
    # REGISTER API BLUEPRINTS
    # -----------------------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(period_predictor_bp, url_prefix="/api/period-predictor")
    app.register_blueprint(schemes_bp)
    app.register_blueprint(ecommerce_bp)
    app.register_blueprint(clinics_bp)

    # -----------------------------------
    # PROMETHEUS MIDDLEWARE
    # -----------------------------------
    @app.before_request
    def before_request():
        g.start_time = time.time()
        HTTP_REQUESTS_IN_PROGRESS.inc()

    @app.after_request
    def after_request(response):
        start_time = getattr(g, "start_time", None)

        if start_time is not None:
            duration = time.time() - start_time

            HTTP_REQUEST_DURATION.labels(
                request.method,
                request.path
            ).observe(duration)

            HTTP_REQUESTS_TOTAL.labels(
                request.method,
                request.path,
                str(response.status_code)
            ).inc()

        HTTP_REQUESTS_IN_PROGRESS.dec()

        return response

    # -----------------------------------
    # PROMETHEUS METRICS ENDPOINT
    # -----------------------------------
    @app.route("/metrics")
    def metrics():
        return generate_latest(), 200, {
            "Content-Type": CONTENT_TYPE_LATEST
        }

    # -----------------------------------
    # HEALTH CHECK
    # -----------------------------------
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Aarohi AI API is running"
        }), 200

    # -----------------------------------
    # FRONTEND ROUTES
    # -----------------------------------
    @app.route("/")
    def index():
        return redirect(url_for("login_page"))

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/chatbot")
    def chatbot_page():
        return redirect(url_for("dashboard_page"))

    @app.route("/period-predictor")
    def period_predictor_page():
        return render_template("period_predictor.html")

    # -----------------------------------
    # PERIOD PREDICTION API
    # -----------------------------------
    @app.route("/api/predict-period", methods=["POST"])
    @jwt_required
    def predict_period_api():
        user_id = g.user_id
        data = request.get_json(silent=True) or {}

        result, error = period_services.run_prediction(user_id, data)

        if error:
            return jsonify({"error": error}), 400

        return jsonify(result)

    return app


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app_host = os.environ.get("FLASK_HOST", "0.0.0.0")
    app_port = int(os.environ.get("FLASK_PORT", 5000))

    app = create_app()
    app.run(
        debug=debug_mode,
        host=app_host,
        port=app_port
    )
