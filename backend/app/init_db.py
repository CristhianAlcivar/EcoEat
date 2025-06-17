from app.core.config import settings
from app.core.database import Base, engine
from app.models.report import Report

print("📡 Connecting to:", settings.DATABASE_URL)

Base.metadata.create_all(bind=engine)