import os
import sys

# Añadimos la carpeta src al PYTHONPATH para que las importaciones funcionen correctamente
sys.path.append('./src')  # Asegúrate de que src está en la ruta correcta

from utils import cargar_datos
from punteo import emparejar_iguales, emparejar_por_suma

def generar_informes(df):
    """
    Genera los informes con los datos punteados y no punteados.
    """
    emparejados = df[df['Indice_Punteo'].notna()]
    no_emparejados = df[df['Indice_Punteo'].isna()]

    # Guardamos los resultados en archivos Excel
    emparejados.to_excel("informes/punteados.xlsx", index=False)
    no_emparejados.to_excel("informes/no_punteados.xlsx", index=False)

    print("Informes generados: punteados.xlsx y no_punteados.xlsx")

def main(ruta_archivo):
    """
    Función principal que orquesta todo el proceso.
    """
    print("Cargando datos...")
    df = cargar_datos(ruta_archivo)
    
    print("Emparejando valores iguales...")
    df = emparejar_iguales(df)
    
    print("Emparejando valores por suma...")
    df = emparejar_por_suma(df)
    
    generar_informes(df)
    print("Proceso completado.")

if __name__ == "__main__":
    archivo = "data/Puntear1.xlsx"  # Cambia esto por el archivo de tu elección
    if os.path.exists(archivo):
        main(archivo)
    else:
        print(f"El archivo {archivo} no se encuentra.")
