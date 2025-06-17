from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import shutil
import uuid
import os

from app.schemas.report import ReportCreate, ReportOut
from app.services.report_service import create_report, get_all_reports
from app.services.image_analysis_service import classify_materials_from_image
from app.ml.classifier import predict_image_class
from app.core.deps import get_db

router = APIRouter()

@router.post("/report", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
def register_report(report: ReportCreate, db: Session = Depends(get_db)):
    return create_report(db, report)

@router.get("/reports", response_model=List[ReportOut])
def list_reports(db: Session = Depends(get_db)):
    return get_all_reports(db)

@router.get("/simulate-image")
def simulate_image_processing(image_name: str):
    """
    Endpoint temporal para simular análisis de una imagen con el modelo IA.
    Usa el nombre del archivo como entrada simulada.
    """
    result = classify_materials_from_image(image_name)
    return result

@router.post("/report-from-image", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
def generate_report_from_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_filename = f"{uuid.uuid4()}.jpg"
    temp_path = os.path.join("temp", temp_filename)
    os.makedirs("temp", exist_ok=True)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = classify_materials_from_image(temp_path)

        report_data = ReportCreate(
            description=result["description"],
            classification=result["classification"],
            estimated_cost=result["estimated_cost"],
            materials=", ".join(result["materials"]),
            confidence_score=result["confidence_score"],
            whatsapp_message="",
            created_at=datetime.now(timezone.utc)
        )

        new_report = create_report(db, report_data=report_data)
        return new_report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/predict-from-image")
def predict_image(file: UploadFile = File(...)):
    try:
        extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        temp_path = os.path.join("temp_uploads", filename)
        os.makedirs("temp_uploads", exist_ok=True)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        classification = predict_image_class(temp_path, mode="garbage")

        if classification == "orgánico":
            classification = f"{classification} - " + predict_image_class(temp_path, mode="food")

        os.remove(temp_path)

        return {"classification": classification}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ping")
def ping():
    return {"message": "pong"}
