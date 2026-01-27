from src.conexion_db import DBConnection
import psycopg2


class UsuarioDAO:

    @staticmethod
    def registrar_usuario(nombre, foto_bytes):
        """Recibe la imagen en bytes y la inserta en la BD"""
        conn = DBConnection.get_connection()  # Pide la conexión al Singleton
        cursor = conn.cursor()
        try:
            # psycopg2.Binary asegura que los bytes se guarden correctamente como BYTEA
            query = "INSERT INTO usuarios (nombre, foto_data) VALUES (%s, %s)"
            cursor.execute(query, (nombre, psycopg2.Binary(foto_bytes)))
            conn.commit()
            print(f"👤 Usuario {nombre} guardado correctamente.")
        except Exception as e:
            conn.rollback()
            print(f"Error en DAO: {e}")
        finally:
            cursor.close()

    @staticmethod
    def obtener_todos():
        """Descarga todos los usuarios y fotos para el entrenamiento"""
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        usuarios = []
        try:
            cursor.execute("SELECT id, nombre, foto_data FROM usuarios")
            usuarios = cursor.fetchall()  # Retorna lista de tuplas
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
        finally:
            cursor.close()
        return usuarios