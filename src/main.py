import os
import shutil
import sys
import pandas as pd  # Asegúrate de importar pandas como pd

# Añadimos la carpeta src al PYTHONPATH para que las importaciones funcionen correctamente
sys.path.append('./src')  # Asegúrate de que src está en la ruta correcta

from utils import cargar_datos
from punteo import emparejar_iguales, emparejar_por_suma, generar_informes

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
        
        # Cargar los datos del archivo Excel
        df = cargar_datos(ruta_archivo)
        
        # Emparejar los valores iguales
        print("Emparejando valores iguales...")
        df = emparejar_iguales(df)
        
        # Emparejar los valores por suma
        print("Emparejando valores por suma...")
        df = emparejar_por_suma(df)
        
        # Aseguramos que los índices de punteo estén ordenados de forma numérica
        df['Indice_Punteo'] = pd.to_numeric(df['Indice_Punteo'], errors='coerce')
        df = df.sort_values(by='Indice_Punteo').reset_index(drop=True)
        
        # Generar los informes de los datos punteados
        generar_informes(df, ruta_archivo)

        # Mover el archivo procesado a la carpeta 'database'
        carpeta_database = "database"
        if not os.path.exists(carpeta_database):
            os.makedirs(carpeta_database)
        
        # Mover archivo a 'database'
        shutil.move(ruta_archivo, os.path.join(carpeta_database, archivo))
        print(f"Archivo {archivo} movido a la carpeta 'database'.")
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()
