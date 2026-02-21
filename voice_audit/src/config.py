import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Clase para centralizar la configuración del sistema """
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "voice_audit_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "admin")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Configuración de seguridad adicional si fuera necesaria
    MAX_INTENTOS = 3