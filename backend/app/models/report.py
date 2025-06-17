from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    materials = Column(String, default="", nullable=False)
    confidence_score = Column(Float, default=0.0, nullable=False)
    whatsapp_message = Column(String, default="", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
