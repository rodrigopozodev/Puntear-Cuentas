import os
import shutil
import sys

# Añadimos la carpeta src al PYTHONPATH
sys.path.append('./src')

from utils import cargar_datos, crear_directorio
from punteo import emparejar_iguales, emparejar_por_suma, generar_informes

def main():
    """Función principal que orquesta todo el proceso."""
    carpeta_data = "data"
    archivos = [f for f in os.listdir(carpeta_data) if f.endswith('.xlsx')]

    if not archivos:
        print(f"No se encontraron archivos Excel en la carpeta {carpeta_data}.")
        return
    
    # Creamos la carpeta database si no existe
    carpeta_database = "database"
    crear_directorio(carpeta_database)
    
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_data, archivo)
        print(f"\nProcesando archivo: {archivo}")
        
        # Procesamiento del archivo
        df = cargar_datos(ruta_archivo)
        print("Emparejando valores iguales...")
        df = emparejar_iguales(df)
        print("Emparejando valores por suma...")
        df = emparejar_por_suma(df)
        
        # Generación de informes
        generar_informes(df, ruta_archivo)

        # Mover archivo procesado
        shutil.move(ruta_archivo, os.path.join(carpeta_database, archivo))
        print(f"Archivo {archivo} movido a la carpeta 'database'.")
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()
