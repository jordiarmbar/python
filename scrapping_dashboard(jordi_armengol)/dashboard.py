import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Libros")
st.title("📚 Dashboard de 'Books to Scrape'")


@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("libros.csv")
        df['Precio'] = df['Precio'].str.replace('£', '').astype(float)

        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        df['Rating_Num'] = df['Rating'].map(rating_map)
        return df

    except FileNotFoundError:
        st.error("Error: Archivo 'libros.csv' no encontrado. Ejecuta 'scraper.py' primero.")
        return None


df = cargar_datos()

if df is None:
    st.stop()

st.sidebar.header("Filtros")
rating_slider = st.sidebar.slider(
    "Selecciona un rango de Rating (estrellas):",
    min_value=1,
    max_value=5,
    value=(1, 5)
)


precio_slider = st.sidebar.slider(
    "Selecciona un rango de Precio (£):",
    min_value=float(df['Precio'].min()),
    max_value=float(df['Precio'].max()),
    value=(float(df['Precio'].min()), float(df['Precio'].max()))
)

df_filtrado = df[
    (df['Rating_Num'] >= rating_slider[0]) &
    (df['Rating_Num'] <= rating_slider[1]) &
    (df['Precio'] >= precio_slider[0]) &
    (df['Precio'] <= precio_slider[1])
    ]


st.subheader("Resumen de Libros Filtrados")
total_libros = df_filtrado.shape[0]
precio_promedio = df_filtrado['Precio'].mean()
rating_promedio = df_filtrado['Rating_Num'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Libros", f"{total_libros}")
col2.metric("Precio Promedio", f"£{precio_promedio:.2f}")
col3.metric("Rating Promedio", f"{rating_promedio:.1f} ★")

st.subheader("Visualizaciones")
col_graf1, col_graf2 = st.columns(2)


fig_ratings = px.histogram(
    df_filtrado,
    x='Rating',
    title='Distribución de Ratings',
    category_orders={"Rating": ["One", "Two", "Three", "Four", "Five"]}
)
col_graf1.plotly_chart(fig_ratings, use_container_width=True)


fig_precio_rating = px.scatter(
    df_filtrado,
    x='Precio',
    y='Rating_Num',
    title='Relación Precio vs. Rating',
    labels={'Rating_Num': 'Rating (Estrellas)'}
)
col_graf2.plotly_chart(fig_precio_rating, use_container_width=True)

st.subheader("Datos de los Libros (filtrados)")
st.dataframe(df_filtrado)