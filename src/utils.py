import pandas as pd
import os
import numpy as np

def cargar_datos(archivo):
    """
    Carga optimizada del archivo Excel con tipos de datos específicos.
    """
    dtypes = {
        'Debe': 'float64',
        'Haber': 'float64'
    }
    
    df = pd.read_excel(
        archivo,
        dtype=dtypes,
        engine='openpyxl',
        na_values=['', 'NA', 'N/A']
    )
    
    # Optimizamos los datos numéricos y redondeamos a 2 decimales
    df['Debe'] = df['Debe'].fillna(0).round(2)
    df['Haber'] = df['Haber'].fillna(0).round(2)
    
    # Limpiamos valores muy pequeños que pueden causar problemas
    df.loc[df['Debe'] < 0.01, 'Debe'] = 0
    df.loc[df['Haber'] < 0.01, 'Haber'] = 0
    
    return df

def crear_directorio(directorio):
    """Crea un directorio si no existe."""
    if not os.path.exists(directorio):
        os.makedirs(directorio)
