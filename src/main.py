import os
import shutil
import sys
import time
import psutil
from tqdm import tqdm

# Añadimos la carpeta src al PYTHONPATH
sys.path.append('./src')

from utils import cargar_datos, crear_directorio
from punteo import emparejar_iguales, emparejar_por_suma, generar_informes

def procesar_archivo(ruta_archivo):
    """Procesa un archivo con monitoreo de rendimiento."""
    inicio = time.time()
    memoria_inicial = psutil.Process().memory_info().rss / 1024 / 1024
    
    print(f"\nMemoria inicial: {memoria_inicial:.2f} MB")
    
    try:
        df = cargar_datos(ruta_archivo)
        total_registros = len(df)
        print(f"Registros cargados: {total_registros:,}")
        
        print("Emparejando valores iguales...")
        df, punteo_index = emparejar_iguales(df)
        print(f"Tiempo parcial: {time.time() - inicio:.2f} segundos")
        
        print("Emparejando valores por suma...")
        # Primera pasada con valores más restrictivos
        df = emparejar_por_suma(df, punteo_index, max_combinaciones=3, tolerancia=0.01)
        
        # Segunda pasada con valores más flexibles para los que quedaron sin puntear
        punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1
        df = emparejar_por_suma(df, punteo_index, max_combinaciones=4, tolerancia=0.02)
        
        # Calculamos el porcentaje de punteo
        punteados = df['Indice_Punteo'].notna().sum()
        porcentaje = (punteados / total_registros) * 100
        
        tiempo_total = time.time() - inicio
        memoria_final = psutil.Process().memory_info().rss / 1024 / 1024
        
        print(f"Registros punteados: {punteados:,} de {total_registros:,} ({porcentaje:.2f}%)")
        print(f"Tiempo total: {tiempo_total:.2f} segundos")
        print(f"Memoria final: {memoria_final:.2f} MB")
        
        return df
        
    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}")
        return None

def main():
    """Función principal optimizada."""
    carpeta_data = "data"
    archivos = [f for f in os.listdir(carpeta_data) if f.endswith('.xlsx')]

    if not archivos:
        print(f"No se encontraron archivos Excel en la carpeta {carpeta_data}.")
        return
    
    carpeta_database = "database"
    crear_directorio(carpeta_database)
    
    for archivo in tqdm(archivos, desc="Procesando archivos"):
        ruta_archivo = os.path.join(carpeta_data, archivo)
        
        df = procesar_archivo(ruta_archivo)
        if df is not None:
            generar_informes(df, ruta_archivo)
            shutil.move(ruta_archivo, os.path.join(carpeta_database, archivo))
            print(f"Archivo {archivo} procesado y movido.")
        
        # Liberamos memoria
        del df
        import gc
        gc.collect()

if __name__ == "__main__":
    main()
