import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("DB_MODE", "external")

def get_connection():
    host = os.getenv("DB_HOST")

    if MODE == "internal":
        host = 'db'

    return mysql.connector.connect(
        host=host,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        auth_plugin=os.getenv('DB_AUTH_PLUGIN')
    )
