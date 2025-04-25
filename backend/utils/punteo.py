import pandas as pd
from tqdm import tqdm

def limpiar_columnas(df):
    columnas = [col.lower() for col in df.columns]

    # Normalizar nombres
    mapeo = {}
    for col in df.columns:
        if col.lower() == "debe":
            mapeo[col] = "Debe"
        elif col.lower() == "haber":
            mapeo[col] = "Haber"

    df = df.rename(columns=mapeo)

    # Rellenar si faltan columnas
    if "Debe" not in df.columns:
        df["Debe"] = 0.0
    if "Haber" not in df.columns:
        df["Haber"] = 0.0

    # Convertir valores
    df["Debe"] = pd.to_numeric(df["Debe"], errors='coerce').fillna(0.0).round(2)
    df["Haber"] = pd.to_numeric(df["Haber"], errors='coerce').fillna(0.0).round(2)

    # Reordenar si fuera necesario
    df.reset_index(drop=True, inplace=True)

    return df

def obtener_filas_no_punteadas(df):
    if "Indice_Punteo" not in df.columns:
        df["Indice_Punteo"] = None

    return df[df["Indice_Punteo"].isna()].copy()

def mostrar_barra_progreso(iterable, descripcion="Procesando"):
    return tqdm(iterable, desc=descripcion, ncols=100)
