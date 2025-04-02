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
    
    # Optimizamos los datos numéricos
    df['Debe'] = df['Debe'].fillna(0).round(2)
    df['Haber'] = df['Haber'].fillna(0).round(2)
    
    return df

def crear_directorio(directorio):
    """Crea un directorio si no existe."""
    if not os.path.exists(directorio):
        os.makedirs(directorio)
