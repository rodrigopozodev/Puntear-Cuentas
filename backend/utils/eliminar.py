import os
import shutil

def eliminar_informes(carpeta_informes):
    if not os.path.exists(carpeta_informes):
        os.makedirs(carpeta_informes)
        return

    for archivo in os.listdir(carpeta_informes):
        ruta = os.path.join(carpeta_informes, archivo)
        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
            elif os.path.isdir(ruta):
                shutil.rmtree(ruta)
        except Exception as e:
            print(f"❌ Error eliminando {ruta}: {e}")
