import pandas as pd

def cargar_datos(archivo):
    # Cargar el archivo Excel
    df = pd.read_excel(archivo)

    # No filtramos ninguna columna aquí, cargamos todo el DataFrame.
    return df
