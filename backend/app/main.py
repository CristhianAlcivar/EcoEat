from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(title="EcoEat Backend")

# Registrar rutas
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "EcoEat Backend activo", "version": settings.APP_VERSION}
