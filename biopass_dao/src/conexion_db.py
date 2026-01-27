import psycopg2
from src.config import Config


class DBConnection:
    _connection = None  # Variable de clase (Singleton)

    @classmethod
    def get_connection(cls):
        # Verifica si ya existe una conexión activa
        if cls._connection is None or cls._connection.closed != 0:
            try:
                # Si no existe, crea una nueva
                cls._connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    port=Config.DB_PORT
                )
                print("✅ Conexión Singleton establecida (o recuperada).")
            except Exception as e:
                print(f"❌ Error conectando a la BD: {e}")
                raise e

        # Devuelve la misma conexión siempre
        return cls._connection