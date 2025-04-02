import pandas as pd
from itertools import combinations

def emparejar_iguales(df):
    """
    Empareja las filas con 'Debe' y 'Haber' idénticos, asignando un índice de punteo.
    """
    df['Indice_Punteo'] = None  # Creamos una nueva columna para los índices de punteo
    punteo_index = 1

    for i, fila in df.iterrows():
        if pd.notna(fila['Indice_Punteo']):
            continue  # Si ya está punteado, saltamos a la siguiente fila

        # Buscar filas donde 'Debe' es igual a 'Haber' y no han sido punteadas
        coincidencia = df[(df['Debe'] == fila['Haber']) & (df['Indice_Punteo'].isna())]

        if not coincidencia.empty:
            idx = coincidencia.index[0]
            df.at[i, 'Indice_Punteo'] = punteo_index
            df.at[idx, 'Indice_Punteo'] = punteo_index
            punteo_index += 1

    return df

def emparejar_por_suma(df):
    """
    Busca combinaciones de sumas en la columna 'Debe' para emparejar con los valores de 'Haber'.
    """
    no_punteados = df[df['Indice_Punteo'].isna()].copy()
    punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1

    for i, fila in no_punteados.iterrows():
        objetivo = fila['Haber']
        candidatos = no_punteados[no_punteados['Debe'] > 0]

        for n in range(2, len(candidatos) + 1):
            for combinacion in combinations(candidatos.index, n):
                suma = sum(df.loc[combinacion, 'Debe'])
                if suma == objetivo:
                    df.loc[combinacion, 'Indice_Punteo'] = punteo_index
                    df.at[i, 'Indice_Punteo'] = punteo_index
                    punteo_index += 1
                    break

    return df
