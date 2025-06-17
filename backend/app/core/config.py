from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = "EcoEat"
    APP_VERSION = "1.0.0"
    
    # 🔥 Define directamente la cadena correcta con el puerto 5455
    DATABASE_URL = "postgresql://root:root@localhost:5455/ecoeat_db"

settings = Settings()
