from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.database import get_db
from backend.app.services.traffic_analytics_service import TrafficAnalyticsService
from backend.app.services.telemetry_monitor import TelemetryBandwidthMonitor

router = APIRouter()

@router.get("/metrics")
def get_city_metrics(db: Session = Depends(get_db)):
    analytics_svc = TrafficAnalyticsService(db)
    congestion_reports = analytics_svc.evaluate_junction_congestion()
    od_matrix = analytics_svc.compute_origin_destination_matrix(time_window_hours=1)
    bandwidth = TelemetryBandwidthMonitor.get_system_bandwidth_metrics(db)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "active_cameras": bandwidth["active_nodes"],
        "congestion_map": congestion_reports,
        "origin_destination_matrix": od_matrix,
        "bandwidth_metrics": bandwidth
    }

@router.get("/telemetry/health")
def get_telemetry_health(db: Session = Depends(get_db)):
    return TelemetryBandwidthMonitor.get_system_bandwidth_metrics(db)

@router.get("/density/geojson")
def get_density_geojson(db: Session = Depends(get_db)):
    analytics_svc = TrafficAnalyticsService(db)
    return analytics_svc.generate_density_geojson()
