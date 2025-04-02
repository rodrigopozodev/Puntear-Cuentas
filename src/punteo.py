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
                suma = sum(candidatos.loc[combinacion, 'Debe'])  # Aquí corregimos el acceso a las filas
                if suma == objetivo:
                    df.loc[combinacion, 'Indice_Punteo'] = punteo_index
                    df.at[i, 'Indice_Punteo'] = punteo_index
                    punteo_index += 1
                    break

    return df

def generar_informes(df):
    """
    Genera los informes con los datos punteados y no punteados, incluyendo todas las columnas del DataFrame.
    """
    emparejados = df[df['Indice_Punteo'].notna()]
    no_emparejados = df[df['Indice_Punteo'].isna()]

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
    archivo = "data/Puntear.xlsx"  # Cambia esto por el archivo de tu elección
    if os.path.exists(archivo):
        main(archivo)
    else:
        print(f"El archivo {archivo} no se encuentra.")
