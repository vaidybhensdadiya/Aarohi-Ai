import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # Flask secret key
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database configuration
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else None

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS")) if os.getenv("JWT_EXPIRATION_HOURS") else None

    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


