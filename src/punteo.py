import pandas as pd
import os
from itertools import combinations

def cargar_datos(ruta_archivo):
    """
    Carga el archivo Excel en un DataFrame.
    """
    return pd.read_excel(ruta_archivo)

def emparejar_iguales(df):
    """
    Empareja las filas con 'Debe' y 'Haber' idénticos, asignando un índice de punteo.
    Ignora las celdas con valor 0.00 en las columnas 'Debe' y 'Haber', pero no ignora la fila completa.
    """
    df['Indice_Punteo'] = None  # Creamos una nueva columna para los índices de punteo
    punteo_index = 1

    for i, fila in df.iterrows():
        if pd.notna(fila['Indice_Punteo']):
            continue  # Si ya está punteado, saltamos a la siguiente fila

        # Si la columna 'Debe' tiene 0, pero 'Haber' tiene valor, se empareja por 'Haber'
        if fila['Debe'] == 0 and fila['Haber'] != 0:
            coincidencia = df[(df['Debe'] == fila['Haber']) & (df['Indice_Punteo'].isna())]
            if not coincidencia.empty:
                idx = coincidencia.index[0]
                df.at[i, 'Indice_Punteo'] = punteo_index
                df.at[idx, 'Indice_Punteo'] = punteo_index
                punteo_index += 1
            continue

        # Si la columna 'Haber' tiene 0, pero 'Debe' tiene valor, se empareja por 'Debe'
        if fila['Haber'] == 0 and fila['Debe'] != 0:
            coincidencia = df[(df['Haber'] == fila['Debe']) & (df['Indice_Punteo'].isna())]
            if not coincidencia.empty:
                idx = coincidencia.index[0]
                df.at[i, 'Indice_Punteo'] = punteo_index
                df.at[idx, 'Indice_Punteo'] = punteo_index
                punteo_index += 1
            continue

        # Buscar filas donde 'Debe' es igual a 'Haber' y no han sido punteadas
        if round(fila['Debe'], 2) == round(fila['Haber'], 2) and fila['Debe'] != 0:
            coincidencia = df[(round(df['Debe'], 2) == round(fila['Haber'], 2)) & (df['Indice_Punteo'].isna())]
            if not coincidencia.empty:
                idx = coincidencia.index[0]
                df.at[i, 'Indice_Punteo'] = punteo_index
                df.at[idx, 'Indice_Punteo'] = punteo_index
                punteo_index += 1

    return df

def emparejar_por_suma(df):
    """
    Busca combinaciones de sumas en la columna 'Debe' para emparejar con los valores de 'Haber'.
    Ignora las celdas con valor 0.00 en las columnas 'Debe' y 'Haber', pero no ignora la fila completa.
    """
    no_punteados = df[df['Indice_Punteo'].isna()].copy()
    punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1

    for i, fila in no_punteados.iterrows():
        # Ignorar celdas con valor 0.00 en 'Debe' o 'Haber'
        if fila['Debe'] == 0 and fila['Haber'] == 0:
            continue

        objetivo = round(fila['Haber'], 2)
        candidatos = no_punteados[no_punteados['Debe'] > 0]

        for n in range(2, len(candidatos) + 1):
            for combinacion in combinations(candidatos.index, n):
                # Acceder a las filas usando los índices de la combinación de manera correcta
                suma = round(sum(candidatos.loc[list(combinacion), 'Debe']), 2)
                if suma == objetivo:
                    # Asignar el índice de punteo a todas las filas de la combinación
                    if df.loc[list(combinacion), 'Indice_Punteo'].isna().all():
                        df.loc[list(combinacion), 'Indice_Punteo'] = punteo_index
                        df.at[i, 'Indice_Punteo'] = punteo_index
                        punteo_index += 1
                    break

    return df

def generar_informes(df):
    """
    Genera los informes con los datos punteados y no punteados, incluyendo todas las columnas del DataFrame
    con la columna Indice_Punteo en la primera posición.
    """
    # Filtramos los datos emparejados y no emparejados, pero conservamos todas las columnas
    emparejados = df[df['Indice_Punteo'].notna()]
    no_emparejados = df[df['Indice_Punteo'].isna()]

    # Insertamos la columna 'Indice_Punteo' al principio de ambos DataFrames sin eliminar otras columnas
    emparejados = pd.concat([emparejados['Indice_Punteo'], emparejados.drop(columns='Indice_Punteo')], axis=1)
    no_emparejados = pd.concat([no_emparejados['Indice_Punteo'], no_emparejados.drop(columns='Indice_Punteo')], axis=1)

    # Guardamos los resultados en archivos Excel con todas las columnas
    emparejados.to_excel("informes/punteados.xlsx", index=False)
    no_emparejados.to_excel("informes/no_punteados.xlsx", index=False)

    print("Informes generados: punteados.xlsx y no_punteados.xlsx")

def main(ruta_archivo):
    """
    Función principal que orquesta todo el proceso.
    """
    print("Cargando datos...")
    df = cargar_datos(ruta_archivo)
    
    print("Emparejando valores iguales...")
    df = emparejar_iguales(df)
    
    print("Emparejando valores por suma...")
    df = emparejar_por_suma(df)
    
    generar_informes(df)
    print("Proceso completado.")

if __name__ == "__main__":
    archivo = "data/puntear1.xlsx"  # Cambia esto por el archivo de tu elección
    if os.path.exists(archivo):
        main(archivo)
    else:
        print(f"El archivo {archivo} no se encuentra.")
