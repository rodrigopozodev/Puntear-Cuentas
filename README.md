python src/main.py
rodri@Rodrigo MINGW64 /c/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/backend
$ node server.js

rm -rf dist
ng build --configuration production
netlify deploy --dir=dist/frontend/browser
