const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const fsPromises = require('fs').promises;
const xlsx = require('xlsx');

const app = express();
app.use(cors());

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const savePath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/data';
    if (!fs.existsSync(savePath)){
      fs.mkdirSync(savePath, { recursive: true });
    }
    cb(null, savePath);
  },
  filename: function (req, file, cb) {
    // Quitar el timestamp y usar solo el nombre original
    cb(null, file.originalname);
  }
});

const upload = multer({ storage: storage });

app.post('/save-excel', upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }
    res.send({ message: 'File uploaded successfully' });
  } catch (error) {
    res.status(500).send(error.message);
  }
});

app.post('/execute-python', (req, res) => {
  // Directorio base del proyecto
  const projectDir = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas';
  
  // Cambiar al directorio del proyecto y ejecutar el comando
  exec('cd "' + projectDir + '" && python src/main.py', {
    shell: 'C:\\Program Files\\Git\\bin\\bash.exe'  // Usar Git Bash
  }, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error ejecutando Python: ${error}`);
      return res.status(500).send(error);
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).send(stderr);
    }
    console.log(`stdout: ${stdout}`);
    res.send({ output: stdout });
  });
});

async function getFilesRecursively(dir) {
  const items = await fsPromises.readdir(dir, { withFileTypes: true });
  let files = [];

  for (const item of items) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      files = files.concat(await getFilesRecursively(fullPath));
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

app.get('/informes/download', async (req, res) => {
  try {
    const filePath = req.query.path;
    if (!filePath) {
      return res.status(400).json({ error: 'No se proporcionó la ruta del archivo' });
    }
    res.download(filePath);
  } catch (error) {
    console.error('Error al descargar archivo:', error);
    res.status(500).json({ error: 'Error al descargar el archivo' });
  }
});

app.get('/informes/content', async (req, res) => {
  try {
    const filePath = req.query.path;
    if (!filePath) {
      return res.status(400).json({ error: 'No se proporcionó la ruta del archivo' });
    }

    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const jsonData = xlsx.utils.sheet_to_json(worksheet);

    const headers = Object.keys(jsonData[0] || {});
    
    res.json({
      headers,
      rows: jsonData
    });
  } catch (error) {
    console.error('Error al leer Excel:', error);
    res.status(500).json({ error: 'Error al leer el archivo Excel' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});