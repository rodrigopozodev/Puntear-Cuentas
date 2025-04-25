import pandas as pd
from itertools import combinations
from tqdm import tqdm
from utils.formato import asignar_indice_punteo
from utils.punteo import limpiar_columnas, obtener_filas_no_punteadas

def nivel_2_punteo(df):
    print("🔁 Ejecutando Nivel 2: Combinaciones de Debe para igualar un Haber...")

    df = limpiar_columnas(df)
    df = asignar_indice_punteo(df)

    no_punteadas = obtener_filas_no_punteadas(df)
    indice_actual = df['Indice_Punteo'].max() if df['Indice_Punteo'].notna().any() else 0
    indice_actual = int(indice_actual)

    usados = set()
    haber_no_usado = no_punteadas[~no_punteadas.index.isin(usados)]

    # Usar tqdm para la barra de progreso
    for idx_haber, fila_haber in tqdm(haber_no_usado.iterrows(), total=len(haber_no_usado), desc="Nivel 2", unit="haber"):
        valor_haber = round(fila_haber['Haber'], 2)

        if valor_haber == 0 or idx_haber in usados:
            continue

        # Filtrar candidatos que no pueden sumar el valor_haber
        candidatos_debe = no_punteadas[
            (~no_punteadas.index.isin(usados)) &
            (no_punteadas['Debe'] > 0) &
            (no_punteadas['Debe'] <= valor_haber)
        ]

        valores_debe = candidatos_debe['Debe'].tolist()
        indices_debe = candidatos_debe.index.tolist()

        # Crear un diccionario para acceder rápidamente a los valores
        valores_dict = dict(zip(indices_debe, valores_debe))

        # Optimización: Usar un enfoque de suma de subconjuntos
        suma_actual = 0
        subconjunto = []
        encontrado = False

        for r in range(1, min(6, len(indices_debe) + 1)):  # Limitar a combinaciones de hasta 5 elementos
            for combo in combinations(indices_debe, r):
                suma = round(sum(valores_dict[i] for i in combo), 2)
                if suma == valor_haber:
                    indice_actual += 1
                    df.at[idx_haber, 'Indice_Punteo'] = indice_actual
                    for i in combo:
                        df.at[i, 'Indice_Punteo'] = indice_actual
                    usados.update([idx_haber] + list(combo))
                    encontrado = True
                    break
            if encontrado:
                break  # Salir si ya se punteó este Haber

    print(f"✅ Nivel 2 completado.")
    return df