# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time
from tqdm import tqdm
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

sys.path.append('./src')

from utils import cargar_datos, crear_directorio
from punteo import emparejar_iguales, emparejar_por_suma, generar_informes

def mostrar_tiempo_estimado(inicio, progreso, total):
    """Calcula y muestra el tiempo estimado restante."""
    tiempo_transcurrido = time.time() - inicio
    if progreso == 0:
        return "Calculando..."
    
    tiempo_estimado_total = (tiempo_transcurrido / progreso) * total
    tiempo_restante = tiempo_estimado_total - tiempo_transcurrido
    return str(timedelta(seconds=int(tiempo_restante)))

def procesar_archivo(ruta_archivo):
    """Procesa un archivo con múltiples pasadas optimizadas."""
    try:
        tiempo_inicio = time.time()
        print(f"\nIniciando procesamiento de {os.path.basename(ruta_archivo)}")
        print("Cargando datos...")
        df = cargar_datos(ruta_archivo)
        total_registros = len(df)
        
        if total_registros > 100000:
            print(f"¡Advertencia! El archivo contiene {total_registros:,} registros, superando el límite de 100,000.")
            return None
        
        print(f"Total de registros a procesar: {total_registros:,}")
        
        # Primera pasada - valores iguales
        print("\nPrimera pasada - Buscando valores exactamente iguales...")
        df, punteo_index = emparejar_iguales(df)
        punteados = df['Indice_Punteo'].notna().sum()
        print(f"→ Registros punteados: {punteados:,} ({(punteados/total_registros*100):.2f}%)")
        
        # Pasadas para combinaciones múltiples
        rangos_combinaciones = [(2,3), (4,5), (6,7), (8,10)]
        
        for idx, (min_comb, max_comb) in enumerate(rangos_combinaciones, 2):
            print(f"\nPasada {idx} - Buscando combinaciones de {min_comb}-{max_comb} registros...")
            registros_antes = df['Indice_Punteo'].notna().sum()
            
            punteo_index = df['Indice_Punteo'].max() + 1 if df['Indice_Punteo'].notna().any() else 1
            df = emparejar_por_suma(df, punteo_index, max_combinaciones=max_comb, tolerancia=0)
            
            punteados = df['Indice_Punteo'].notna().sum()
            nuevos = punteados - registros_antes
            print(f"→ Nuevos registros punteados: {nuevos:,}")
            print(f"→ Total punteados: {punteados:,} ({(punteados/total_registros*100):.2f}%)")
        
        tiempo_total = time.time() - tiempo_inicio
        print(f"\nResultados finales:")
        print(f"→ Registros punteados: {punteados:,} de {total_registros:,} ({(punteados/total_registros*100):.2f}%)")
        print(f"→ Tiempo total de procesamiento: {str(timedelta(seconds=int(tiempo_total)))}")
        
        return df
        
    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}")
        return None

def main():
    """Función principal con control de progreso mejorado."""
    carpeta_data = "data"
    archivos = [f for f in os.listdir(carpeta_data) if f.endswith('.xlsx')]

    if not archivos:
        print(f"No se encontraron archivos Excel en la carpeta {carpeta_data}.")
        return
    
    print(f"Se encontraron {len(archivos)} archivos para procesar.")
    carpeta_database = "database"
    crear_directorio(carpeta_database)
    
    for i, archivo in enumerate(archivos, 1):
        print(f"\n{'='*80}")
        print(f"Procesando archivo {i} de {len(archivos)}: {archivo}")
        print('='*80)
        
        ruta_archivo = os.path.join(carpeta_data, archivo)
        df = procesar_archivo(ruta_archivo)
        
        if df is not None:
            print("\nGenerando informes...")
            generar_informes(df, ruta_archivo)
            shutil.move(ruta_archivo, os.path.join(carpeta_database, archivo))
            print(f"Archivo {archivo} procesado y movido exitosamente.")
        
        # Liberamos memoria
        del df
        import gc
        gc.collect()

if __name__ == "__main__":
    main()
