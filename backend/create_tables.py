from app.core.database import Base, engine
from app.models.report import Report

def recreate_tables():
    try:
        print("🧹 Borrando y creando tablas...")

        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print("✅ Tablas creadas correctamente.")
    except Exception as e:
        print("❌ Error al crear las tablas:", e)

if __name__ == "__main__":
    recreate_tables()
