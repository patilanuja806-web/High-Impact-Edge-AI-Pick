from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from backend.app.database import Base

class VehicleSighting(Base):
    __tablename__ = "vehicle_sightings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(String(32), ForeignKey("camera_nodes.camera_id"), index=True, nullable=False)
    plate_number = Column(String(16), index=True, nullable=False)
    clean_plate_number = Column(String(16), index=True, nullable=False)
    confidence = Column(Float, nullable=False)
    vehicle_class = Column(String(32), default="Unknown")
    vehicle_color = Column(String(32), default="Unknown")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    image_base64 = Column(Text, nullable=True)
    track_id = Column(String(64), nullable=True, index=True)
