from sqlalchemy.orm import Session
from app.models.report import Report
from app.schemas.report import ReportCreate


def create_report(db: Session, report_data: ReportCreate) -> Report:
    report = Report(
        description=report_data.description,
        classification=report_data.classification,
        estimated_cost=report_data.estimated_cost,
        materials=report_data.materials,
        confidence_score=report_data.confidence_score,
        whatsapp_message=report_data.whatsapp_message,
        created_at=report_data.created_at
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_all_reports(db: Session):
    return db.query(Report).order_by(Report.created_at.desc()).all()
