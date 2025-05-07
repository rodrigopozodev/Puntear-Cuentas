from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

from funciones.Nivel_1_Punteo import nivel_1_punteo
from funciones.Nivel_2_Punteo import nivel_2_punteo
from funciones.Nivel_3_Punteo import nivel_3_punteo
from utils.cors import configurar_cors

from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

import os
import shutil
import glob
import pandas as pd

# Rutas
CARPETA_SUBIDOS = "archivos/subidos"
CARPETA_PROCESADOS = "archivos/procesados"
CARPETA_INFORMES = "archivos/informes"

app = FastAPI()
configurar_cors(app)  # <-- Aplicar configuración de CORS

def obtener_archivo_excel():
    archivos = glob.glob(os.path.join(CARPETA_SUBIDOS, "*.xlsx"))
    return archivos[0] if archivos else None

def mover_a_procesados(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)
    nueva_ruta = os.path.join(CARPETA_PROCESADOS, nombre_archivo)
    shutil.move(ruta_archivo, nueva_ruta)

@app.post("/subir")
async def subir_archivo(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".xlsx"):
            return JSONResponse(content={"error": "Solo se permiten archivos .xlsx"}, status_code=400)

        ruta_guardado = os.path.join(CARPETA_SUBIDOS, file.filename)
        with open(ruta_guardado, "wb") as f:
            contenido = await file.read()
            f.write(contenido)

        return {"mensaje": f"Archivo '{file.filename}' subido correctamente."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/procesar")
def procesar_archivo():
    try:
        archivo = obtener_archivo_excel()
        if not archivo:
            return JSONResponse(content={"mensaje": "No se encontró ningún archivo para procesar."}, status_code=404)

        df = pd.read_excel(archivo)

        df = nivel_1_punteo(df)
        df = nivel_2_punteo(df)
        df = nivel_3_punteo(df)

        punteados = df[df['Indice_Punteo'].notna()]
        no_punteados = df[df['Indice_Punteo'].isna()]

        punteados.to_excel(os.path.join(CARPETA_INFORMES, "Punteados.xlsx"), index=False)
        no_punteados.to_excel(os.path.join(CARPETA_INFORMES, "No_Punteados.xlsx"), index=False)

        mover_a_procesados(archivo)

        return {"mensaje": "Proceso finalizado correctamente."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
