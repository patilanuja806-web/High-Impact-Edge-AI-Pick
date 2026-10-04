from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate_number = Column(String(16), unique=True, index=True, nullable=False)
    case_reference = Column(String(64), nullable=False)
    crime_category = Column(String(64), nullable=False)
    severity_level = Column(String(16), default="CRITICAL")
    created_at = Column(DateTime, default=datetime.utcnow)
