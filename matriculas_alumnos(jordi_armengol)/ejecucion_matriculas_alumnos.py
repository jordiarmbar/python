from dominio.alumno import Alumno
from servicio.alumnos_matriculados import AlumnosMatriculados
import sys

def main():
    print("")
    print("Menú de Gestión de Matrículas:")
    print("1- Matricular alumno")
    print("2- Listar alumnos")
    print("3- Eliminar archivo de alumnos")
    print("4- Salir")

def ejecutar_opcion(opcion:str):
    if opcion == "1":
        nombre = input("Introduce el nombre del alumno a matricular: ")
        nuevo_alumno = Alumno(nombre)
        AlumnosMatriculados.matricular_alumno(nuevo_alumno)

    elif opcion == "2":
        alumnos = AlumnosMatriculados.listar_alumnos()
        print("Lista de alumnos:")
        if alumnos:
            for i, nombre in enumerate(alumnos, 1):
                print(f"{i}. {nombre}")
        else:
            print("No hay alumnos matriculados.")
    elif opcion == "3":
        confirmacion = input("¿Estás seguro de que quieres ELIMINAR el archivo de alumnos? (s/n): ").lower()
        if confirmacion == 's':
            AlumnosMatriculados.eliminar_alumno()
        else:
            print("Operación de eliminación cancelada.")
    elif opcion == '4':
        sys.exit(0)
    else:
        print("Opción no válida")

if __name__ == "__main__":
    while True:
        main()
        opcion = input("Elige una opción: ")
        ejecutar_opcion(opcion)