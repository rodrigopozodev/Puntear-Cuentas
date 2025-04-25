import pandas as pd
from utils.formato import asignar_indice_punteo
from utils.punteo import limpiar_columnas, obtener_filas_no_punteadas
from tqdm import tqdm  # Importar tqdm

def nivel_1_punteo(df):
    print("🔍 Ejecutando Nivel 1: Coincidencias exactas entre Debe y Haber...")

    df = limpiar_columnas(df)
    df = asignar_indice_punteo(df)  # Asegura columna 'Indice_Punteo' existe

    no_punteadas = obtener_filas_no_punteadas(df)

    usado = set()
    indice_actual = df['Indice_Punteo'].max() if df['Indice_Punteo'].notna().any() else 0
    indice_actual = int(indice_actual)

    # Convertir columnas a listas para mejorar el rendimiento
    indices = no_punteadas.index.tolist()
    valores_debe = no_punteadas['Debe'].round(2).tolist()
    valores_haber = no_punteadas['Haber'].round(2).tolist()

    punteadas = []  # Lista para almacenar las filas punteadas

    # Usar tqdm para la barra de progreso
    for i in tqdm(range(len(indices)), desc="Nivel 1", unit="fila"):
        if indices[i] in usado or valores_debe[i] == 0:
            continue

        for j in range(len(indices)):
            if i == j or indices[j] in usado or valores_haber[j] == 0:
                continue

            if valores_debe[i] == valores_haber[j]:
                indice_actual += 1
                df.at[indices[i], 'Indice_Punteo'] = indice_actual
                df.at[indices[j], 'Indice_Punteo'] = indice_actual
                usado.update([indices[i], indices[j]])
                punteadas.append((indices[i], indices[j]))
                break

    print(f"✅ Nivel 1 completado. {len(usado)//2} pares punteados.")
    print(f"🔗 Filas punteadas en Nivel 1: {punteadas}")
    return df
