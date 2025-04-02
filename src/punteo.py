import pandas as pd
import os
from itertools import combinations
from utils import cargar_datos, crear_directorio

def emparejar_iguales(df):
    """
    Empareja las filas con 'Debe' y 'Haber' idénticos.
    """
    df['Indice_Punteo'] = None
    punteo_index = 1
    
    for i, fila in df[df['Indice_Punteo'].isna()].iterrows():
        if fila['Debe'] == 0 and fila['Haber'] != 0:
            coincidencia = df[(df['Debe'] == fila['Haber']) & (df['Indice_Punteo'].isna())]
        elif fila['Haber'] == 0 and fila['Debe'] != 0:
            coincidencia = df[(df['Haber'] == fila['Debe']) & (df['Indice_Punteo'].isna())]
        elif round(fila['Debe'], 2) == round(fila['Haber'], 2) and fila['Debe'] != 0:
            coincidencia = df[(round(df['Debe'], 2) == round(fila['Haber'], 2)) & (df['Indice_Punteo'].isna())]
        else:
            continue

        if not coincidencia.empty:
            idx = coincidencia.index[0]
            df.at[i, 'Indice_Punteo'] = punteo_index
            df.at[idx, 'Indice_Punteo'] = punteo_index
            punteo_index += 1
    
    return df

def emparejar_por_suma(df):
    """
    Busca combinaciones de sumas en la columna 'Debe' para emparejar con 'Haber'.
    """
    no_punteados = df[df['Indice_Punteo'].isna()].copy()
    punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1

    for i, fila in no_punteados.iterrows():
        if fila['Debe'] == 0 and fila['Haber'] == 0:
            continue
        
        objetivo = round(fila['Haber'], 2)
        candidatos = no_punteados[no_punteados['Debe'] > 0]

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
    """Genera los informes con los datos punteados y no punteados."""
    # Ordenamos el DataFrame por Indice_Punteo
    df['Indice_Punteo'] = pd.to_numeric(df['Indice_Punteo'], errors='coerce')
    df = df.sort_values(by='Indice_Punteo')

    # Filtramos los datos
    emparejados = df[df['Indice_Punteo'].notna()]
    no_emparejados = df[df['Indice_Punteo'].isna()]

    # Configuramos las rutas
    nombre_base = os.path.basename(archivo).replace(".xlsx", "")
    carpeta_informes = "informes"
    subcarpeta_informes = os.path.join(carpeta_informes, nombre_base)
    
    # Creamos las carpetas necesarias
    crear_directorio(carpeta_informes)
    crear_directorio(subcarpeta_informes)

    # Generamos los informes
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
        
        generar_informes(df, ruta_archivo)
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()
