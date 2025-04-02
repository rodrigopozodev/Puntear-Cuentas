import os
import pandas as pd
import numpy as np
from itertools import combinations
from utils import cargar_datos, crear_directorio

def emparejar_iguales(df):
    """
    Versión optimizada para emparejar valores iguales usando vectorización.
    """
    df['Indice_Punteo'] = None
    punteo_index = 1
    
    # Creamos máscaras para filtrado eficiente
    no_punteados = df['Indice_Punteo'].isna()
    
    # Procesamos por lotes para mejor rendimiento
    while no_punteados.any():
        fila = df[no_punteados].iloc[0]
        
        if fila['Debe'] > 0 and fila['Haber'] == 0:
            mask = (df['Haber'] == fila['Debe']) & no_punteados & (df.index != fila.name)
        elif fila['Haber'] > 0 and fila['Debe'] == 0:
            mask = (df['Debe'] == fila['Haber']) & no_punteados & (df.index != fila.name)
        else:
            no_punteados[fila.name] = False
            continue
            
        if mask.any():
            idx_match = df[mask].index[0]
            df.loc[[fila.name, idx_match], 'Indice_Punteo'] = punteo_index
            punteo_index += 1
            no_punteados[fila.name] = False
            no_punteados[idx_match] = False
        else:
            no_punteados[fila.name] = False
            
    return df

def emparejar_por_suma(df, max_combinaciones=3, chunk_size=100):
    """
    Versión optimizada para buscar combinaciones de sumas.
    """
    no_punteados = df[df['Indice_Punteo'].isna()].copy()
    punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1
    
    # Ordenamos por valor para optimizar búsqueda
    debe_valores = no_punteados[no_punteados['Debe'] > 0].sort_values('Debe', ascending=False)
    haber_valores = no_punteados[no_punteados['Haber'] > 0].sort_values('Haber', ascending=False)
    
    # Procesamos por chunks los valores de Haber
    for _, haber_fila in haber_valores.iterrows():
        objetivo = round(haber_fila['Haber'], 2)
        if objetivo == 0:
            continue
            
        # Filtramos candidatos potenciales
        candidatos = debe_valores[
            (debe_valores['Debe'] <= objetivo) & 
            (debe_valores.index != haber_fila.name)
        ].head(50)  # Limitamos candidatos para mejor rendimiento
        
        if len(candidatos) < 2:
            continue
            
        # Convertimos a array numpy para cálculos más rápidos
        valores = candidatos['Debe'].values
        
        # Buscamos combinaciones eficientemente
        for n in range(2, min(max_combinaciones + 1, len(valores) + 1)):
            encontrado = False
            for comb in combinations(range(len(valores)), n):
                suma = round(np.sum(valores[list(comb)]), 2)
                if suma == objetivo:
                    indices = candidatos.index[list(comb)]
                    if df.loc[indices, 'Indice_Punteo'].isna().all():
                        df.loc[indices, 'Indice_Punteo'] = punteo_index
                        df.at[haber_fila.name, 'Indice_Punteo'] = punteo_index
                        punteo_index += 1
                        encontrado = True
                        break
            if encontrado:
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
