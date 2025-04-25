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

    punteadas = []  # Lista para almacenar las filas punteadas

    for idx_haber, fila_haber in tqdm(haber_no_usado.iterrows(), total=len(haber_no_usado), desc="Nivel 2", unit="haber"):
        valor_haber = round(fila_haber['Haber'], 2)

        if valor_haber == 0 or idx_haber in usados:
            continue

        candidatos_debe = no_punteadas[
            (~no_punteadas.index.isin(usados)) &
            (no_punteadas['Debe'] > 0)
        ]

        if candidatos_debe.empty:
            continue

        valores_debe = candidatos_debe['Debe']
        indices_debe = candidatos_debe.index.tolist()

        for r in range(1, min(16, len(indices_debe) + 1)):
            for combo in combinations(indices_debe, r):
                suma = round(sum(df.loc[i, 'Debe'] for i in combo), 2)
                if suma == valor_haber:
                    indice_actual += 1
                    df.at[idx_haber, 'Indice_Punteo'] = indice_actual
                    for i in combo:
                        df.at[i, 'Indice_Punteo'] = indice_actual
                    usados.update([idx_haber] + list(combo))
                    punteadas.append((idx_haber, list(combo)))
                    break
            else:
                continue
            break

    print(f"✅ Nivel 2 completado. {len(punteadas)} combinaciones punteadas.")
    print(f"🔗 Filas punteadas en Nivel 2: {punteadas}")
    return df