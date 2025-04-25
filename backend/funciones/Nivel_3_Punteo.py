import pandas as pd
from itertools import combinations
from tqdm import tqdm
from utils.formato import asignar_indice_punteo
from utils.punteo import limpiar_columnas, obtener_filas_no_punteadas

def nivel_3_punteo(df):
    print("🔄 Ejecutando Nivel 3: Combinaciones de Haber para igualar un Debe...")

    df = limpiar_columnas(df)
    df = asignar_indice_punteo(df)

    no_punteadas = obtener_filas_no_punteadas(df)
    indice_actual = df['Indice_Punteo'].max() if df['Indice_Punteo'].notna().any() else 0
    indice_actual = int(indice_actual)

    usados = set()
    debe_no_usado = no_punteadas[~no_punteadas.index.isin(usados)]

    punteadas = []  # Lista para almacenar las filas punteadas

    for idx_debe, fila_debe in tqdm(debe_no_usado.iterrows(), total=len(debe_no_usado), desc="Nivel 3", unit="debe"):
        valor_debe = round(fila_debe['Debe'], 2)

        if valor_debe == 0 or idx_debe in usados:
            continue

        candidatos_haber = no_punteadas[
            (~no_punteadas.index.isin(usados)) &
            (no_punteadas['Haber'] > 0)
        ]

        if candidatos_haber.empty:
            continue

        valores_haber = candidatos_haber['Haber']
        indices_haber = candidatos_haber.index.tolist()

        for r in range(1, min(16, len(indices_haber) + 1)):
            for combo in combinations(indices_haber, r):
                suma = round(sum(df.loc[i, 'Haber'] for i in combo), 2)
                if suma == valor_debe:
                    indice_actual += 1
                    df.at[idx_debe, 'Indice_Punteo'] = indice_actual
                    for i in combo:
                        df.at[i, 'Indice_Punteo'] = indice_actual
                    usados.update([idx_debe] + list(combo))
                    punteadas.append((idx_debe, list(combo)))
                    break
            else:
                continue
            break

    print(f"✅ Nivel 3 completado. {len(punteadas)} combinaciones punteadas.")
    print(f"🔗 Filas punteadas en Nivel 3: {punteadas}")
    return df