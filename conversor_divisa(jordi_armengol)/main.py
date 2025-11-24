import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox



def cargar_datos():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


    tasas = {'EUR': 1.0}
    fecha = "Desconocida"

    try:

        response = requests.get(url)

        if response.status_code == 200:
            print("Conexión exitosa.")


            root = ET.fromstring(response.content)


            ns = {'ecb': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}


            cube_time = root.find('.//ecb:Cube/ecb:Cube', ns)
            if cube_time is not None:
                fecha = cube_time.attrib.get('time')


            for cube in root.findall('.//ecb:Cube', ns):
                if 'currency' in cube.attrib:
                    moneda = cube.attrib['currency']
                    tasa = float(cube.attrib['rate'])
                    tasas[moneda] = tasa

            return fecha, tasas

        else:
            print("Error al conectar con el servidor.")
            messagebox.showerror("Error", "Error al conectar con el servidor.")
            return None, None

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
        return None, None



def realizar_calculo():
    try:
        cantidad = float(entry_cantidad.get())
        moneda_origen = combo_origen.get()
        moneda_destino = combo_destino.get()


        tasa_origen = datos_tasas[moneda_origen]
        tasa_destino = datos_tasas[moneda_destino]


        resultado = (cantidad / tasa_origen) * tasa_destino


        lbl_resultado.config(text=f"{resultado:.2f} {moneda_destino}")

    except ValueError:
        messagebox.showwarning("Atención", "Introduce un número válido.")



root = tk.Tk()
root.title("Conversor de Divisas (BCE)")
root.geometry("400x400")


fecha_datos, datos_tasas = cargar_datos()

if datos_tasas:

    lista_monedas = sorted(list(datos_tasas.keys()))


    tk.Label(root, text=f"Datos actualizados: {fecha_datos}", fg="green").pack(pady=10)

    tk.Label(root, text="Cantidad a convertir:").pack()
    entry_cantidad = tk.Entry(root)
    entry_cantidad.pack(pady=5)

    tk.Label(root, text="De (Moneda Origen):").pack()
    combo_origen = ttk.Combobox(root, values=lista_monedas, state="readonly")
    combo_origen.set("EUR")
    combo_origen.pack(pady=5)

    tk.Label(root, text="A (Moneda Destino):").pack()
    combo_destino = ttk.Combobox(root, values=lista_monedas, state="readonly")
    combo_destino.set("USD")
    combo_destino.pack(pady=5)

    btn_calcular = tk.Button(root, text="Calcular", command=realizar_calculo, bg="#e1e1e1")
    btn_calcular.pack(pady=20)

    lbl_resultado = tk.Label(root, text="Resultados aquí", font=("Arial", 14, "bold"))
    lbl_resultado.pack()

else:
    tk.Label(root, text="No se pudieron cargar los datos XML.", fg="red").pack(pady=20)


root.mainloop()