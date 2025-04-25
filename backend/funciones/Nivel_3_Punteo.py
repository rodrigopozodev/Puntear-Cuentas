import pandas as pd
from itertools import combinations
from tqdm import tqdm
from utils.formato import asignar_indice_punteo
from utils.punteo import limpiar_columnas, obtener_filas_no_punteadas, mostrar_barra_progreso

def nivel_3_punteo(df):
    print("🔄 Ejecutando Nivel 3: Combinaciones de Haber para igualar un Debe...")

    df = limpiar_columnas(df)
    df = asignar_indice_punteo(df)

    no_punteadas = obtener_filas_no_punteadas(df)
    indice_actual = df['Indice_Punteo'].max() if df['Indice_Punteo'].notna().any() else 0
    indice_actual = int(indice_actual)

    usados = set()
    debe_no_usado = no_punteadas[~no_punteadas.index.isin(usados)]

    # Usar tqdm para la barra de progreso
    for idx_debe, fila_debe in tqdm(debe_no_usado.iterrows(), total=len(debe_no_usado), desc="Nivel 3", unit="debe"):
        valor_debe = round(fila_debe['Debe'], 2)

        if valor_debe == 0 or idx_debe in usados:
            continue

        # Filtrar candidatos que no pueden sumar el valor_debe
        candidatos_haber = no_punteadas[
            (~no_punteadas.index.isin(usados)) &
            (no_punteadas['Haber'] > 0) &
            (no_punteadas['Haber'] <= valor_debe)
        ]

        valores_haber = candidatos_haber['Haber'].tolist()
        indices_haber = candidatos_haber.index.tolist()

        # Crear un diccionario para acceder rápidamente a los valores
        valores_dict = dict(zip(indices_haber, valores_haber))

        # Optimización: Usar un enfoque de suma de subconjuntos
        suma_actual = 0
        subconjunto = []
        encontrado = False

        for r in range(1, min(6, len(indices_haber) + 1)):  # Limitar a combinaciones de hasta 5 elementos
            for combo in combinations(indices_haber, r):
                suma = round(sum(valores_dict[i] for i in combo), 2)
                if suma == valor_debe:
                    indice_actual += 1
                    df.at[idx_debe, 'Indice_Punteo'] = indice_actual
                    for i in combo:
                        df.at[i, 'Indice_Punteo'] = indice_actual
                    usados.update([idx_debe] + list(combo))
                    encontrado = True
                    break
            if encontrado:
                break  # Salir si ya se punteó este Debe

    print(f"✅ Nivel 3 completado.")
    return df