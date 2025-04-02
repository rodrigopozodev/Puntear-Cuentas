import pandas as pd

def cargar_datos(archivo):
    # Cargar el archivo Excel
    df = pd.read_excel(archivo)

    # Muestra las primeras filas y las columnas para depuración (esto es opcional)
    # print("Columnas disponibles:", df.columns)
    # print("Primeras filas:", df.head())

    # Filtra las columnas necesarias sin la columna 'Fecha'
    df = df[['Debe', 'Haber']]  # Filtramos solo 'Debe' y 'Haber'

    return df
