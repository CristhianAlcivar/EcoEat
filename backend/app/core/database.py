from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Configuración de conexión
engine = create_engine(settings.DATABASE_URL, echo=True)

# Sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()
