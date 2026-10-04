from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RouteLeg(BaseModel):
    from_camera: str
    to_camera: str
    from_coords: List[float]
    to_coords: List[float]
    departure_time: datetime
    arrival_time: datetime
    speed_kmh: float
    distance_meters: float
    reconciled: bool = False
    reconciliation_details: Optional[str] = None
    snapshot_thumbnail: Optional[str] = None

class NextJunctionPrediction(BaseModel):
    predicted_junction: str
    junction_name: str
    coordinates: List[float]
    probability: float
    eta_window_minutes: str

class TrajectoryReconstructionResponse(BaseModel):
    queried_plate: str
    canonical_plate: str
    total_legs: int
    legs: List[RouteLeg]
    prediction: Optional[NextJunctionPrediction] = None
    status: str
