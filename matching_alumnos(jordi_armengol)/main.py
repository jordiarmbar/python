import csv

FILE_UF1 = 'Notas_alumnos_UF1.csv'
FILE_UF2 = 'Notas_alumnos_UF2.csv'
FILE_SALIDA = 'notas_alumnos.csv'
SEPARADOR = ';'
columnas_finales = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2']
datos_alumnos = {}


print(f"Iniciando... Leyendo {FILE_UF1}")


try:

    with open(FILE_UF1, mode='r') as file:
        reader = csv.DictReader(file, delimiter = SEPARADOR)

        for fila in reader:
            id_alumno = fila['Id']
            datos_alumnos[id_alumno] = fila

except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo {FILE_UF1}")
    exit()
except Exception as e:
    print(f"Ha ocurrido un error inesperado leyendo {FILE_UF1}: {e}")
    exit()

print(f"Lectura de UF1 completada. Leyendo {FILE_UF2}...")


try:
    with open(FILE_UF2, mode='r') as file:
        reader = csv.DictReader(file, delimiter=SEPARADOR)

        for fila in reader:
            id_alumno = fila['Id']

            if id_alumno in datos_alumnos:
                datos_alumnos[id_alumno]['UF2'] = fila['UF2']
            else:
                print(f"Aviso: Alumno con Id {id_alumno} en UF2 no encontrado en UF1.")

except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo {FILE_UF2}")
    exit()
except Exception as e:
    print(f"Ha ocurrido un error inesperado leyendo {FILE_UF2}: {e}")
    exit()

print("Combinación de datos completada. Escribiendo archivo final...")


try:

    with open(FILE_SALIDA, mode='w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=columnas_finales, delimiter=SEPARADOR)
        writer.writeheader()
        writer.writerows(datos_alumnos.values())

except PermissionError:
    print(f"No tienes permisos para escribir en {FILE_SALIDA}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado escribiendo {FILE_SALIDA}: {e}")

print(f"¡Proceso finalizado! Se ha creado el archivo '{FILE_SALIDA}' con éxito.")