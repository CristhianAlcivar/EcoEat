from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
