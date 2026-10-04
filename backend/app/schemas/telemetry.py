from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SightingIngestRequest(BaseModel):
    camera_id: str = Field(..., example="CAM_JNC_A")
    plate_number: str = Field(..., min_length=4, max_length=16, example="DL01AB1234")
    raw_ocr_plate: Optional[str] = Field(None, example="DLO1AB1284")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.94)
    vehicle_class: str = Field(default="Car", example="Car")
    vehicle_color: str = Field(default="White", example="White")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    image_base64: Optional[str] = Field(None, description="Base64 thumbnail string")

class CameraHeartbeat(BaseModel):
    camera_id: str
    fps: float
    status: str = "ONLINE"
    bandwidth_kbps: float = 2.4
