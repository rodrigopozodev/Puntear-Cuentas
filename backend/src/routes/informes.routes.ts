import { Router } from 'express';
import * as fs from 'fs/promises';
import * as path from 'path';

const router = Router();

router.delete('/delete-informes-folder', async (req, res) => {
  const informesPath = path.join(process.cwd(), 'informes');
  
  try {
    // Verificamos si la carpeta existe
    const exists = await fs.access(informesPath)
      .then(() => true)
      .catch(() => false);

    if (exists) {
      // Borramos recursivamente todos los archivos y la carpeta
      await fs.rm(informesPath, { recursive: true, force: true });
      
      // Creamos la carpeta de nuevo vacía
      await fs.mkdir(informesPath);
      
      res.status(200).send({ message: 'Carpeta de informes borrada y recreada correctamente' });
    } else {
      // Si no existe, solo creamos la carpeta
      await fs.mkdir(informesPath);
      res.status(200).send({ message: 'Carpeta de informes creada correctamente' });
    }
  } catch (error) {
    console.error('Error al borrar la carpeta de informes:', error);
    res.status(500).send({ error: 'Error al borrar la carpeta de informes' });
  }
});

export default router;
