import os
import pymysql
from config import Config

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv('DB_HOST', 'mysql-service'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR (database.py):", e)
        return None

