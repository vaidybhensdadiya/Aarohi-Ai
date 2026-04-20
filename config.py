import os

class Config:
    # Flask secret key
    SECRET_KEY = "aarohi-ai-secret-key"

    # Database configuration
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "Vaidy@2005"
    DB_NAME = "aarohi_ai"
    DB_PORT = 3306

    # JWT configuration
    JWT_SECRET_KEY = "aarohi-ai-jwt-secret"
    JWT_EXPIRATION_HOURS = 24

    # Gemini API (add later)
    GEMINI_API_KEY ="AIzaSyD-Hsd_NC4GWlnKzdbuOt7YW7fANbwjyW4"

