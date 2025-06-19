from fastapi import APIRouter, Query

from app.data.repositories.image_repository_impl import SQLAlchemyImageRepository
from app.data.db.database import SessionLocal
from fastapi import UploadFile, File

router = APIRouter(prefix="/imagenes", tags=["imagenes"])

@router.post("/clasificar")
def clasificar_imagen(file: UploadFile = File(...), usuario_id: str = ""):
    import uuid, os, shutil
    from app.application.use_cases.clasificar_materiales import ClasificarMaterialesUseCase
    from app.data.ml.material_detector import MaterialDetector
    from app.application.use_cases.guardar_imagen_clasificada import GuardarImagenClasificadaUseCase
    from app.data.repositories.image_repository_impl import SQLAlchemyImageRepository

    # Guardar temporalmente la imagen
    image_id = str(uuid.uuid4())
    save_path = f"temp/{image_id}_{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ejecutar modelo de predicción
    detector = MaterialDetector("data/model/modelo_ecoat.h5")
    clasificador = ClasificarMaterialesUseCase(detector)
    resultado = clasificador.execute(save_path)

    # Usar función para contar renovables y no renovables
    renovables, no_renovables = detector.contar_tipo_materiales(resultado)
    confianza = sum(resultado.values()) / len(resultado)

    # Guardar resultado si se especifica el usuario
    if usuario_id:
        repo = SQLAlchemyImageRepository()
        guardar = GuardarImagenClasificadaUseCase(repo)
        guardar.execute({
            "id": image_id,
            "nombre_imagen": file.filename,
            "ruta": save_path,
            "usuario_id": usuario_id,
            "resultado_modelo": resultado,
            "materiales_renovables": renovables,
            "materiales_no_renovables": no_renovables,
            "confianza_promedio": confianza
        })

    return {
        "resultado": resultado,
        "renovables": renovables,
        "no_renovables": no_renovables,
        "confianza_promedio": confianza
    }


@router.get("/")
def listar_todas_con_usuario(telefono: str = Query(None)):
    with SessionLocal() as session:
        repo = SQLAlchemyImageRepository(session)
        if telefono:
            if telefono.startswith("0") and len(telefono) == 10:
                telefono = "593" + telefono[1:]
            return repo.get_all_with_user(telefono)
        return repo.get_all_with_user()