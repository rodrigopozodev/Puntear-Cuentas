from fastapi.middleware.cors import CORSMiddleware

def configurar_cors(app):
    origins = [
        "http://localhost:4200",
        "https://tu-dominio-angular.com"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
