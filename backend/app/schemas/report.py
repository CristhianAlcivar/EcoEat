from pydantic import BaseModel
from datetime import datetime

class ReportBase(BaseModel):
    description: str
    classification: str
    estimated_cost: float
    materials: str
    confidence_score: float
    whatsapp_message: str

class ReportCreate(ReportBase):
    created_at: datetime

class ReportOut(ReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
