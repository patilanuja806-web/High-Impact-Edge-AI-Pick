from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from backend.app.database import get_db
from backend.app.models.camera import CameraNode
from backend.app.models.sighting import VehicleSighting
from backend.app.models.vehicle_track import VehicleTrajectorySegment
from backend.app.schemas.analytics import CityTrafficAnalyticsResponse, CongestionMetric, OriginDestinationFlow

router = APIRouter()

@router.get("/metrics", response_model=CityTrafficAnalyticsResponse)
def get_city_metrics(db: Session = Depends(get_db)):
    cams = db.query(CameraNode).all()
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    congestion_list = []
    for c in cams:
        count = (
            db.query(VehicleSighting)
            .filter(VehicleSighting.camera_id == c.camera_id, VehicleSighting.timestamp >= one_hour_ago)
            .count()
        )
        density_per_min = count / 60.0
        status = "GREEN"
        early_warn = False
        if density_per_min > 8.0:
            status = "RED"
            early_warn = True
        elif density_per_min > 4.0:
            status = "ORANGE"

        congestion_list.append(CongestionMetric(
            junction_code=c.junction_code,
            current_status=status,
            vehicle_density_per_min=round(density_per_min, 1),
            avg_speed_kmh=42.5,
            early_bottleneck_warning=early_warn
        ))

    od_query = (
        db.query(
            VehicleTrajectorySegment.from_camera_id,
            VehicleTrajectorySegment.to_camera_id,
            func.count(VehicleTrajectorySegment.id).label("flow_count"),
            func.avg(VehicleTrajectorySegment.speed_kmh).label("avg_spd")
        )
        .group_by(VehicleTrajectorySegment.from_camera_id, VehicleTrajectorySegment.to_camera_id)
        .order_by(func.count(VehicleTrajectorySegment.id).desc())
        .limit(5)
        .all()
    )

    cam_map = {c.camera_id: c.name for c in cams}
    flows = [
        OriginDestinationFlow(
            origin=cam_map.get(od[0], od[0]),
            destination=cam_map.get(od[1], od[1]),
            vehicle_count=od[2],
            avg_transit_minutes=round(od[3] if od[3] else 2.5, 1)
        )
        for od in od_query
    ]

    total_today = db.query(VehicleSighting).count()
    return CityTrafficAnalyticsResponse(
        timestamp=datetime.utcnow().isoformat(),
        active_cameras=len([c for c in cams if c.is_active]),
        total_vehicles_detected_today=total_today,
        congestion_map=congestion_list,
        top_od_flows=flows
    )
