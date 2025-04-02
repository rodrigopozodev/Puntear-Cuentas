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
    df['Indice_Punteo'] = None  # Inicializamos la columna de punteo
    punteo_index = 1
    
    # Buscamos coincidencias en las columnas 'Debe' y 'Haber'
    for i, fila in df[df['Indice_Punteo'].isna()].iterrows():
        if fila['Debe'] == 0 and fila['Haber'] != 0:
            coincidencia = df[(df['Debe'] == fila['Haber']) & (df['Indice_Punteo'].isna())]
        elif fila['Haber'] == 0 and fila['Debe'] != 0:
            coincidencia = df[(df['Haber'] == fila['Debe']) & (df['Indice_Punteo'].isna())]
        elif round(fila['Debe'], 2) == round(fila['Haber'], 2) and fila['Debe'] != 0:
            coincidencia = df[(round(df['Debe'], 2) == round(fila['Haber'], 2)) & (df['Indice_Punteo'].isna())]
        else:
            continue  # Si no hay coincidencia, pasamos al siguiente

        # Si encontramos coincidencias, asignamos el índice de punteo
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

    # Iteramos solo sobre las filas que no han sido punteadas
    for i, fila in no_punteados.iterrows():
        if fila['Debe'] == 0 and fila['Haber'] == 0:
            continue  # Ignoramos filas con 'Debe' y 'Haber' a 0
        
        objetivo = round(fila['Haber'], 2)
        candidatos = no_punteados[no_punteados['Debe'] > 0]

        # Usamos combinaciones para encontrar sumas que coincidan con el valor de 'Haber'
        for n in range(2, len(candidatos) + 1):
            for combinacion in combinations(candidatos.index, n):
                suma = round(sum(candidatos.loc[list(combinacion), 'Debe']), 2)
                if suma == objetivo:
                    if df.loc[list(combinacion), 'Indice_Punteo'].isna().all():
                        df.loc[list(combinacion), 'Indice_Punteo'] = punteo_index
                        df.at[i, 'Indice_Punteo'] = punteo_index
                        punteo_index += 1
                    break

    return df

def generar_informes(df, archivo):
    """
    Genera los informes con los datos punteados y no punteados.
    """
    # Filtramos los datos emparejados y no emparejados
    emparejados = df[df['Indice_Punteo'].notna()]
    no_emparejados = df[df['Indice_Punteo'].isna()]

    # Añadimos la columna 'Indice_Punteo' al final, sin cambiar el orden de las filas
    emparejados = emparejados[emparejados.columns.tolist() + ['Indice_Punteo']]
    no_emparejados = no_emparejados[no_emparejados.columns.tolist() + ['Indice_Punteo']]

    # Creamos la carpeta 'informes' si no existe
    carpeta_informes = "informes"
    if not os.path.exists(carpeta_informes):
        os.makedirs(carpeta_informes)

    # Usamos el nombre del archivo para crear una subcarpeta
    nombre_base = os.path.basename(archivo).replace(".xlsx", "")
    subcarpeta_informes = os.path.join(carpeta_informes, nombre_base)
    if not os.path.exists(subcarpeta_informes):
        os.makedirs(subcarpeta_informes)

    # Se generan los informes para cada archivo
    emparejados.to_excel(f"{subcarpeta_informes}/{nombre_base}_punteados.xlsx", index=False)
    no_emparejados.to_excel(f"{subcarpeta_informes}/{nombre_base}_no_punteados.xlsx", index=False)

    print(f"Informes generados para {archivo}: {nombre_base}_punteados.xlsx y {nombre_base}_no_punteados.xlsx")

def main():
    """
    Función principal que orquesta todo el proceso.
    """
    carpeta_data = "data"  # Carpeta donde se encuentran los archivos Excel
    archivos = [f for f in os.listdir(carpeta_data) if f.endswith('.xlsx')]

    if not archivos:
        print(f"No se encontraron archivos Excel en la carpeta {carpeta_data}.")
        return
    
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_data, archivo)
        print(f"\nProcesando archivo: {archivo}")
        df = cargar_datos(ruta_archivo)
        
        print("Emparejando valores iguales...")
        df = emparejar_iguales(df)
        
        print("Emparejando valores por suma...")
        df = emparejar_por_suma(df)
        
        # Aseguramos que los índices de punteo estén ordenados de forma numérica
        df['Indice_Punteo'] = pd.to_numeric(df['Indice_Punteo'], errors='coerce')
        df = df.sort_values(by='Indice_Punteo').reset_index(drop=True)
        
        generar_informes(df, ruta_archivo)
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()
