import os

class Config:
    # Flask secret key for sessions and cookies
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_default_secret_key')
    
    # Database configurations parsed by your app
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

