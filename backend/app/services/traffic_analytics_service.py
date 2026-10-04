from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models.camera import CameraNode
from backend.app.models.sighting import VehicleSighting
from backend.app.models.vehicle_track import VehicleTrajectorySegment

class TrafficAnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def compute_origin_destination_matrix(self, time_window_hours: int = 1) -> List[Dict[str, Any]]:
        since_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        flows = (
            self.db.query(
                VehicleTrajectorySegment.from_camera_id,
                VehicleTrajectorySegment.to_camera_id,
                func.count(VehicleTrajectorySegment.id).label("trip_count"),
                func.avg(VehicleTrajectorySegment.speed_kmh).label("mean_speed_kmh"),
                func.avg(VehicleTrajectorySegment.distance_meters).label("mean_dist_m")
            )
            .filter(VehicleTrajectorySegment.start_time >= since_time)
            .group_by(VehicleTrajectorySegment.from_camera_id, VehicleTrajectorySegment.to_camera_id)
            .order_by(func.count(VehicleTrajectorySegment.id).desc())
            .all()
        )

        cams = {c.camera_id: c.name for c in self.db.query(CameraNode).all()}
        od_results = []

        for flow in flows:
            dist_km = (flow.mean_dist_m or 1500) / 1000.0
            spd = flow.mean_speed_kmh if flow.mean_speed_kmh and flow.mean_speed_kmh > 0 else 40.0
            avg_transit_min = round((dist_km / spd) * 60.0, 1)

            od_results.append({
                "origin_id": flow.from_camera_id,
                "origin_name": cams.get(flow.from_camera_id, flow.from_camera_id),
                "destination_id": flow.to_camera_id,
                "destination_name": cams.get(flow.to_camera_id, flow.to_camera_id),
                "volume": flow.trip_count,
                "average_speed_kmh": round(spd, 1),
                "transit_duration_minutes": avg_transit_min
            })

        return od_results

    def evaluate_junction_congestion(self) -> List[Dict[str, Any]]:
        cams = self.db.query(CameraNode).all()
        ten_mins_ago = datetime.utcnow() - timedelta(minutes=10)
        thirty_mins_ago = datetime.utcnow() - timedelta(minutes=30)

        congestion_reports = []

        for cam in cams:
            short_term_count = (
                self.db.query(VehicleSighting)
                .filter(VehicleSighting.camera_id == cam.camera_id, VehicleSighting.timestamp >= ten_mins_ago)
                .count()
            )
            baseline_count = (
                self.db.query(VehicleSighting)
                .filter(VehicleSighting.camera_id == cam.camera_id, VehicleSighting.timestamp >= thirty_mins_ago)
                .count()
            )

            current_rate = short_term_count / 10.0
            historical_rate = baseline_count / 30.0

            early_warning = current_rate > 1.5 * historical_rate and current_rate > 5.0
            
            if current_rate >= 8.0:
                level = "RED"
            elif current_rate >= 4.0:
                level = "ORANGE"
            else:
                level = "GREEN"

            congestion_reports.append({
                "camera_id": cam.camera_id,
                "junction_name": cam.name,
                "junction_code": cam.junction_code,
                "latitude": cam.latitude,
                "longitude": cam.longitude,
                "density_per_minute": round(current_rate, 2),
                "congestion_level": level,
                "early_bottleneck_warning": early_warning
            })

        return congestion_reports

    def generate_density_geojson(self) -> Dict[str, Any]:
        congestion_data = self.evaluate_junction_congestion()
        features = []

        for c in congestion_data:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [c["longitude"], c["latitude"]]
                },
                "properties": {
                    "junction": c["junction_name"],
                    "density": c["density_per_minute"],
                    "level": c["congestion_level"],
                    "weight": 1.0 if c["congestion_level"] == "RED" else (0.6 if c["congestion_level"] == "ORANGE" else 0.2)
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }
