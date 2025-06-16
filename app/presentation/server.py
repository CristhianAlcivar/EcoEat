from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.users import router as usuarios_router
from app.presentation.images import router as imagenes_router
from app.presentation.ecobot import router as ecobot_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Ecoat API",
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
    
    return app

app = create_app()
