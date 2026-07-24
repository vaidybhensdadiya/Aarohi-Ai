import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # Flask secret key
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database configuration
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME", "aarohi_ai")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", 24))

    # Gemini API
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


