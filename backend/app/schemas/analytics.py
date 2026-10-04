from pydantic import BaseModel
from typing import List

class OriginDestinationFlow(BaseModel):
    origin: str
    destination: str
    vehicle_count: int
    avg_transit_minutes: float

class CongestionMetric(BaseModel):
    junction_code: str
    current_status: str
    vehicle_density_per_min: float
    avg_speed_kmh: float
    early_bottleneck_warning: bool

class CityTrafficAnalyticsResponse(BaseModel):
    timestamp: str
    active_cameras: int
    total_vehicles_detected_today: int
    congestion_map: List[CongestionMetric]
    top_od_flows: List[OriginDestinationFlow]
