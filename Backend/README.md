# Excel Matching App

Este proyecto es una aplicación diseñada para realizar el punteo entre columnas de archivos Excel, específicamente entre las columnas "Debe" y "Haber". La aplicación permite tres tipos de punteo: completo, debe y haber.

## Estructura del Proyecto

```
Backend
├── src
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── utils
│   │   ├── excel_reader.py     # Funciones para leer archivos Excel
│   │   ├── matcher.py          # Lógica para realizar el punteo
│   │   └── logger.py           # Manejo de registro de eventos y errores
│   └── tests
│       ├── test_excel_reader.py # Pruebas unitarias para excel_reader.py
│       ├── test_matcher.py      # Pruebas unitarias para matcher.py
│       └── test_logger.py       # Pruebas unitarias para logger.py
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
└── .gitignore                  # Archivos y directorios a ignorar por Git
```

## Instalación

Para instalar las dependencias necesarias, ejecuta el siguiente comando en la raíz del proyecto:

```
pip install -r requirements.txt
```

## Uso

1. Asegúrate de tener los archivos Excel que deseas puntear.
2. Ejecuta la aplicación desde el archivo `main.py`:

```
python src/main.py
```

3. Sigue las instrucciones en la consola para cargar los archivos y realizar el punteo.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.
