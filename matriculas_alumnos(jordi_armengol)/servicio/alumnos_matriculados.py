from dominio.alumno import Alumno
import os

class AlumnosMatriculados:

    RUTA_ARCHIVO: str = "alumnos.txt"

    @staticmethod
    def matricular_alumno(alumno: Alumno):

        try:
            with open(AlumnosMatriculados.RUTA_ARCHIVO, 'a') as f:
                f.write(f"{alumno.nombre}\n")
            print(f"{alumno.nombre} ha sido matriculado con éxito.")
        except IOError as e:
            print(f"Error al escribir en {e}")

    @staticmethod
    def listar_alumnos() -> list[str]:
        alumnos = []
        try:
            if not os.path.exists(AlumnosMatriculados.RUTA_ARCHIVO):
                print("ℹ️ El archivo de alumnos no existe aún.")
                return alumnos

            with open(AlumnosMatriculados.RUTA_ARCHIVO, 'r') as f:
                alumnos = [line.strip() for line in f if line.strip()]
        except IOError as e:
            print(f"Error al leer el archivo: {e}")
        return alumnos

    @staticmethod
    def eliminar_alumno():

        try:
            if os.path.exists(AlumnosMatriculados.RUTA_ARCHIVO):
                os.remove(AlumnosMatriculados.RUTA_ARCHIVO)
                print("Archivo eliminado")
            else:
                print("El archivo no existe")
        except OSError as e:
            print(f"Error al eliminar el archivo: {e}")