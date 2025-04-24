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
    
    return df

def crear_directorio(directorio):
    """Crea un directorio si no existe."""
    if not os.path.exists(directorio):
        os.makedirs(directorio)
