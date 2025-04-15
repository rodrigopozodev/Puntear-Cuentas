// Este código es un servidor backend con Node.js usando Express, que permite subir archivos Excel, ejecuta un script de Python, y gestiona archivos de informes.

//📦 Importación de dependencias
const express = require('express');               // Framework web para crear el servidor.
const multer = require('multer');                 // Middleware para manejar la subida de archivos.
const cors = require('cors');                     // Permite peticiones entre dominios (Cross-Origin Resource Sharing).
const path = require('path');                     // Utilidades para manejar rutas de archivos/directorios.
const fs = require('fs');                         // Módulo de sistema de archivos (sin promesas).
const { exec, spawn } = require('child_process'); // Permite ejecutar comandos o procesos como Python desde Node.
const fsPromises = require('fs').promises;        // Sistema de archivos con soporte para async/await.
const xlsx = require('xlsx');                     // Biblioteca para leer y escribir archivos Excel.

//🚀 Inicialización de Express y CORS
const app = express();     // Crea una app de Express.
app.use(cors());           // Habilita CORS para permitir llamadas desde el frontend.


//📁 Crear carpetas necesarias si no existen
const requiredPaths = [
  'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/data',
  'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes'
];

requiredPaths.forEach(path => {
  if (!fs.existsSync(path)) {
    fs.mkdirSync(path, { recursive: true });  // Crea la carpeta y sus padres si no existen.
    console.log(`Carpeta creada: ${path}`);   // Muestra en consola que se creó la carpeta.
  }
});

//📂 Configuración de Multer para subir archivos
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const savePath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/data';
    if (!fs.existsSync(savePath)){
      fs.mkdirSync(savePath, { recursive: true });
    }
    cb(null, savePath); // Define dónde guardar el archivo.
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname); // Guarda el archivo con su nombre original.
  }
});

const upload = multer({ storage: storage }); // Inicializa el middleware con la configuración anterior.

//📤 Ruta para subir archivos Excel
app.post('/save-excel', upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.'); // Devuelve error si no se subió archivo.
    }
    res.send({ message: 'File uploaded successfully' }); // Respuesta OK.
  } catch (error) {
    res.status(500).send(error.message); // Error general.
  }
});

//🐍 Ruta para ejecutar script Python
app.post('/execute-python', (req, res) => {
  const projectDir = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas';
  
  console.log('Ejecutando script Python...');
  
  const pythonProcess = spawn('python', ['src/main.py'], {
    cwd: projectDir,
    shell: true,
    env: { ...process.env, PYTHONIOENCODING: 'utf-8' } // Asegura codificación correcta.
  });

  let output = '';
  let errorOutput = '';

  pythonProcess.stdout.setEncoding('utf-8');
  pythonProcess.stderr.setEncoding('utf-8');

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
    output += data;
  });

  pythonProcess.stderr.on('data', (data) => {
    console.log(`Python stderr: ${data}`);
    // Ignora mensajes de progreso
    if (!data.includes('Procesando valores:')) {
      errorOutput += data;
    }
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    if (code === 0 && !errorOutput.includes('Error en el procesamiento')) {
      res.json({ success: true, output: output });
    } else {
      res.status(500).json({
        error: true,
        message: 'Error en el script Python',
        details: errorOutput || output
      });
    }
  });
});

//🔍 Función auxiliar para listar archivos Excel recursivamente
async function getFilesRecursively(dir) {
  const items = await fsPromises.readdir(dir, { withFileTypes: true });
  let files = [];

  for (const item of items) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      files = files.concat(await getFilesRecursively(fullPath)); // Llama recursivamente.
    } else if (item.isFile() && (item.name.endsWith('.xlsx') || item.name.endsWith('.xls'))) {
      const stats = await fsPromises.stat(fullPath);
      files.push({
        name: item.name,
        path: fullPath,
        folder: path.relative('C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes', dir),
        size: stats.size,
        createdAt: stats.birthtime
      });
    }
  }
  return files;
}

//📂 Ruta para listar informes disponibles
app.get('/informes', async (req, res) => {
  try {
    const informesPath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes';
    const files = await getFilesRecursively(informesPath);
    res.json(files);
  } catch (error) {
    console.error('Error al leer informes:', error);
    res.status(500).json({ error: 'Error al leer los informes' });
  }
});

//📥 Ruta para descargar un archivo específico
app.get('/informes/download', async (req, res) => {
  try {
    const filePath = req.query.path;
    if (!filePath) {
      return res.status(400).json({ error: 'No se proporcionó la ruta del archivo' });
    }
    res.download(filePath); // Envía el archivo como descarga.
  } catch (error) {
    console.error('Error al descargar archivo:', error);
    res.status(500).json({ error: 'Error al descargar el archivo' });
  }
});

//📖 Ruta para leer contenido de un archivo Excel
app.get('/informes/content', async (req, res) => {
  try {
    const filePath = req.query.path;
    if (!filePath) {
      return res.status(400).json({ error: 'No se proporcionó la ruta del archivo' });
    }

    const workbook = xlsx.readFile(filePath);                      // Abre el archivo.
    const sheetName = workbook.SheetNames[0];                      // Usa la primera hoja.
    const worksheet = workbook.Sheets[sheetName];                 
    const jsonData = xlsx.utils.sheet_to_json(worksheet);         // Lo transforma a JSON.

    const headers = Object.keys(jsonData[0] || {});               // Obtiene los encabezados.
    
    res.json({ headers, rows: jsonData });                        // Devuelve contenido en JSON.
  } catch (error) {
    console.error('Error al leer Excel:', error);
    res.status(500).json({ error: 'Error al leer el archivo Excel' });
  }
});

//❌ Ruta para borrar todos los informes (archivos)
app.delete('/informes', async (req, res) => {
  try {
    const informesPath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes';
    const files = await fsPromises.readdir(informesPath);
    
    for (const file of files) {
      await fsPromises.unlink(path.join(informesPath, file)); // Borra cada archivo.
    }
    
    res.json({ message: 'Informes borrados exitosamente' });
  } catch (error) {
    console.error('Error al borrar informes:', error);
    res.status(500).json({ error: 'Error al borrar los informes' });
  }
});

//🧹 Ruta para reiniciar completamente la carpeta informes
app.delete('/delete-informes-folder', async (req, res) => {
  try {
    const informesPath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes';
    
    try {
      await fsPromises.rm(informesPath, { recursive: true, force: true }); // Borra carpeta completa.
      console.log('Carpeta informes eliminada exitosamente');
    } catch (rmError) {
      console.warn('Error al intentar borrar la carpeta:', rmError);
      // Si falla, usa comando del sistema (Windows).
      await new Promise((resolve, reject) => {
        exec(`rmdir /s /q "${informesPath}"`, (error) => {
          if (error) reject(error);
          else resolve(true);
        });
      });
    }

    await fsPromises.mkdir(informesPath, { recursive: true }); // Crea carpeta nueva.
    console.log('Nueva carpeta informes creada');

    res.json({ message: 'Carpeta de informes reiniciada correctamente' });
  } catch (error) {
    console.error('Error al reiniciar la carpeta de informes:', error);
    res.status(500).json({ 
      error: 'Error al reiniciar la carpeta de informes',
      details: error.message
    });
  }
});

//🔊 Inicio del servidor
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
