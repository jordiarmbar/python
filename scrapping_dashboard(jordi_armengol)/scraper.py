
import requests
import pandas as pd
from bs4 import BeautifulSoup

print("Iniciando el scraper...")


URL = "http://books.toscrape.com/"

titulos = []
precios = []
ratings = []


try:
    pagina = requests.get(URL)
    pagina.raise_for_status()
    print(f"Conexión exitosa a {URL}")

    soup = BeautifulSoup(pagina.content, 'html.parser')


    libros = soup.find_all('article', class_='product_pod')
    print(f"Se encontraron {len(libros)} libros en la página.")


    for libro in libros:

        titulo = libro.h3.a['title']
        precio = libro.find('p', class_='price_color').text
        rating = libro.find('p', class_='star-rating')['class'][1]


        titulos.append(titulo)
        precios.append(precio)
        ratings.append(rating)

    print("Datos extraídos con éxito.")

    datos = {
        'Titulo': titulos,
        'Precio': precios,
        'Rating': ratings
    }

    df = pd.DataFrame(datos)
    df.to_csv('libros.csv', index=False)

    print(f"Archivo 'libros.csv' creado")

except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la web: {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")