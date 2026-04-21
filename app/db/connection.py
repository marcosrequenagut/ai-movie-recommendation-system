import psycopg2
from pgvector.psycopg2 import register_vector
import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "movies_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

def get_connection():
    """
    Returns a connection to the PostgreSQL database using the configuration defined in DB_CONFIG.
    """

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        register_vector(conn)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise