from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_id = Column(String(64), nullable=False)
    action = Column(String(64), nullable=False)
    target_plate = Column(String(16), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
