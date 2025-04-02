const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

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
    cb(null, Date.now() + '-' + file.originalname);
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
  const pythonScript = path.join('C:', 'Users', 'rodri', 'Desktop', 'Mis Proyectos', 'Puntear Cuentas', 'src', 'main.py');
  
  exec(`python "${pythonScript}"`, (error, stdout, stderr) => {
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

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});