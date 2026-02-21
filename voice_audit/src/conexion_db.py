import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            try:
                cls._instancia.conn = psycopg2.connect(
                    host=os.getenv("DB_HOST", "localhost"),
                    database=os.getenv("DB_NAME", "voice_audit_db"),
                    user=os.getenv("DB_USER", "postgres"),
                    password=os.getenv("DB_PASS", "admin"),
                    port=os.getenv("DB_PORT", "5432")
                )
            except Exception as e:
                print(f"Error al conectar a PostgreSQL: {e}")
                cls._instancia.conn = None
        return cls._instancia

    def get_connection(self):
        return self.conn