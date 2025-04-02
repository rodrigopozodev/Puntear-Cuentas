import pandas as pd

def cargar_datos(ruta_archivo):
    """
    Carga los datos del archivo Excel y filtra las columnas relevantes.
    Elimina filas con valores 0 en las columnas 'Debe' o 'Haber'.
    """
    df = pd.read_excel(ruta_archivo)
    # Filtramos las columnas relevantes y eliminamos filas con valores 0
    df = df[['Fecha', 'Debe', 'Haber']]  # Asegúrate de que estas columnas sean correctas
    df = df[(df['Debe'] != 0) | (df['Haber'] != 0)]  # Ignorar filas con valores 0
    return df
