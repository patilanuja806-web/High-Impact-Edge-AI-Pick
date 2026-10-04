from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from backend.app.database import Base

class VehicleTrajectorySegment(Base):
    __tablename__ = "vehicle_trajectory_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    canonical_plate = Column(String(16), index=True, nullable=False)
    from_camera_id = Column(String(32), ForeignKey("camera_nodes.camera_id"), nullable=False)
    to_camera_id = Column(String(32), ForeignKey("camera_nodes.camera_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    speed_kmh = Column(Float, nullable=False)
    distance_meters = Column(Float, nullable=False)
    is_reconciled = Column(Integer, default=0)
    reconciliation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
