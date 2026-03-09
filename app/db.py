import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("No se encontró DATABASE_URL en el archivo .env")
    return psycopg.connect(database_url)

def get_admin_connection():
    admin_database_url = os.getenv("ADMIN_DATABASE_URL")
    if not admin_database_url:
        raise ValueError("No se encontró ADMIN_DATABASE_URL en el archivo .env")
    return psycopg.connect(admin_database_url)