import os
import pandas as pd
import numpy as np
from itertools import combinations
from utils import cargar_datos, crear_directorio

def emparejar_iguales(df):
    """Versión ultra optimizada para emparejar valores iguales."""
    df['Indice_Punteo'] = None
    punteo_index = 1
    
    # Creamos diccionarios para búsqueda O(1)
    debe_dict = {}
    haber_dict = {}
    
    # Construimos índices para búsqueda rápida con tolerancia
    tolerancia = 0.01
    for idx, row in df.iterrows():
        debe = round(row['Debe'], 2)
        haber = round(row['Haber'], 2)
        
        if debe > 0:
            # Agregamos el valor exacto y valores cercanos
            for valor in [debe, round(debe - tolerancia, 2), round(debe + tolerancia, 2)]:
                if valor not in debe_dict:
                    debe_dict[valor] = []
                debe_dict[valor].append(idx)
                
        if haber > 0:
            for valor in [haber, round(haber - tolerancia, 2), round(haber + tolerancia, 2)]:
                if valor not in haber_dict:
                    haber_dict[valor] = []
                haber_dict[valor].append(idx)
    
    # Buscamos coincidencias con tolerancia
    valores_debe = set(debe_dict.keys())
    valores_haber = set(haber_dict.keys())
    
    for valor_debe in valores_debe:
        for valor_haber in valores_haber:
            if abs(valor_debe - valor_haber) <= tolerancia:
                debe_indices = debe_dict[valor_debe]
                haber_indices = haber_dict[valor_haber]
                
                for debe_idx in debe_indices:
                    if df.at[debe_idx, 'Indice_Punteo'] is not None:
                        continue
                    
                    for haber_idx in haber_indices:
                        if (df.at[haber_idx, 'Indice_Punteo'] is None and 
                            debe_idx != haber_idx):
                            df.loc[[debe_idx, haber_idx], 'Indice_Punteo'] = punteo_index
                            punteo_index += 1
                            break
    
    return df, punteo_index

def emparejar_por_suma(df, punteo_index, max_combinaciones=4, tolerancia=0.02):
    """Versión optimizada para buscar combinaciones de sumas."""
    no_punteados = df[df['Indice_Punteo'].isna()].copy()
    
    # Ordenamos y filtramos previamente
    debe_valores = no_punteados[no_punteados['Debe'] > 0].sort_values('Debe', ascending=False)
    haber_valores = no_punteados[no_punteados['Haber'] > 0].sort_values('Haber', ascending=False)
    
    # Convertimos a arrays numpy para mejor rendimiento
    debe_array = debe_valores['Debe'].values
    debe_indices = debe_valores.index.values
    
    # Procesamos primero los valores más grandes de Haber
    for _, haber_fila in haber_valores.iterrows():
        objetivo = round(haber_fila['Haber'], 2)
        if objetivo == 0:
            continue
        
        # Buscamos primero combinaciones exactas, luego con tolerancia
        for tol in [0.0, tolerancia/2, tolerancia]:
            # Filtrado más eficiente con tolerancia progresiva
            mask = debe_array <= (objetivo * (1 + tol))
            valores_filtrados = debe_array[mask]
            indices_filtrados = debe_indices[mask]
            
            if len(valores_filtrados) < 2:
                continue
            
            # Aumentamos el número de candidatos
            n_candidates = min(50, len(valores_filtrados))
            valores_filtrados = valores_filtrados[:n_candidates]
            indices_filtrados = indices_filtrados[:n_candidates]
            
            # Búsqueda optimizada de combinaciones
            encontrado = False
            for n in range(2, min(max_combinaciones + 1, len(valores_filtrados) + 1)):
                if encontrado:
                    break
                    
                for comb_indices in combinations(range(len(valores_filtrados)), n):
                    suma = round(np.sum(valores_filtrados[list(comb_indices)]), 2)
                    if abs(suma - objetivo) <= tol:
                        indices = indices_filtrados[list(comb_indices)]
                        if df.loc[indices, 'Indice_Punteo'].isna().all():
                            df.loc[indices, 'Indice_Punteo'] = punteo_index
                            df.at[haber_fila.name, 'Indice_Punteo'] = punteo_index
                            punteo_index += 1
                            debe_array = np.delete(debe_array, [list(comb_indices)])
                            debe_indices = np.delete(debe_indices, [list(comb_indices)])
                            break
                
            if encontrado:
                break
    
    return df

def generar_informes(df, archivo):
    """Genera los informes con los datos punteados y no punteados."""
    # Eliminamos la ordenación por Indice_Punteo
    df['Indice_Punteo'] = pd.to_numeric(df['Indice_Punteo'], errors='coerce')

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
