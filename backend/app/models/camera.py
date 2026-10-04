from sqlalchemy import Column, String, Float, Boolean, DateTime
from datetime import datetime
from backend.app.database import Base

class CameraNode(Base):
    __tablename__ = "camera_nodes"

    camera_id = Column(String(32), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    junction_code = Column(String(32), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    stream_url = Column(String(256), nullable=True)
    is_active = Column(Boolean, default=True)
    fps_current = Column(Float, default=0.0)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
