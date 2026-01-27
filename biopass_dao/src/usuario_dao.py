from src.conexion_db import DBConnection
import psycopg2


class UsuarioDAO:

    @staticmethod
    def registrar_usuario(nombre, foto_bytes):

        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:

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

        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        usuarios = []
        try:
            cursor.execute("SELECT id, nombre, foto_data FROM usuarios")
            usuarios = cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
        finally:
            cursor.close()
        return usuarios