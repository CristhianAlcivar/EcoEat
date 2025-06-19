from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.users import router as usuarios_router
from app.presentation.images import router as imagenes_router
from app.presentation.ecobot import router as ecobot_router
from app.presentation.materials import router as materiales_router
from app.presentation.models import router as modelos_router
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ecoeat API",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(usuarios_router)
    app.include_router(imagenes_router)
    app.include_router(ecobot_router)
    app.include_router(materiales_router)
    app.include_router(modelos_router)
    
    app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

    return app

app = create_app()
