import os
import shutil
import glob
import pandas as pd

from funciones.Nivel_1_Punteo import nivel_1_punteo
from funciones.Nivel_2_Punteo import nivel_2_punteo
from funciones.Nivel_3_Punteo import nivel_3_punteo
from utils.eliminar import eliminar_informes

# Rutas
CARPETA_SUBIDOS = "archivos/subidos"
CARPETA_PROCESADOS = "archivos/procesados"
CARPETA_INFORMES = "archivos/informes"

def obtener_archivo_excel():
    archivos = glob.glob(os.path.join(CARPETA_SUBIDOS, "*.xlsx"))
    return archivos[0] if archivos else None

def mover_a_procesados(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)
    nueva_ruta = os.path.join(CARPETA_PROCESADOS, nombre_archivo)
    shutil.move(ruta_archivo, nueva_ruta)

def main():
    print("⏳ Iniciando procesamiento...")

    # 1. Eliminar informes anteriores
    eliminar_informes(CARPETA_INFORMES)

    # 2. Obtener archivo
    archivo = obtener_archivo_excel()
    if not archivo:
        print("⚠️ No se encontró ningún archivo en 'archivos/subidos/'")
        return

    print(f"📄 Archivo encontrado: {archivo}")

    # 3. Leer el archivo Excel
    df = pd.read_excel(archivo)

    # 4. Ejecutar punteo nivel 1, 2 y 3
    df = nivel_1_punteo(df)
    df = nivel_2_punteo(df)
    df = nivel_3_punteo(df)

    # 5. Guardar resultados
    punteados = df[df['Indice_Punteo'].notna()]
    no_punteados = df[df['Indice_Punteo'].isna()]

    punteados.to_excel(os.path.join(CARPETA_INFORMES, "Punteados.xlsx"), index=False)
    no_punteados.to_excel(os.path.join(CARPETA_INFORMES, "No_Punteados.xlsx"), index=False)

    # 6. Mover archivo original a procesados
    mover_a_procesados(archivo)

    print("✅ Proceso finalizado correctamente.")

if __name__ == "__main__":
    main()
