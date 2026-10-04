from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.database import get_db
from backend.app.models.camera import CameraNode
from backend.app.schemas.telemetry import SightingIngestRequest, CameraHeartbeat
from backend.app.services.trajectory_service import TrajectoryService
from backend.app.services.alert_service import WatchlistAlertManager
from backend.app.api.websocket import ws_manager

router = APIRouter()

@router.post("/sighting")
async def ingest_sighting(payload: SightingIngestRequest, db: Session = Depends(get_db)):
    cam = db.query(CameraNode).filter(CameraNode.camera_id == payload.camera_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="Camera node not registered")

    traj_service = TrajectoryService(db)
    sighting, reconciled, reason = traj_service.reconcile_and_record_sighting(payload)
    alert = WatchlistAlertManager.check_and_alert(sighting.clean_plate_number, cam.name, db)

    event = {
        "event_type": "NEW_SIGHTING",
        "camera_id": cam.camera_id,
        "camera_name": cam.name,
        "plate_number": sighting.clean_plate_number,
        "raw_plate": payload.raw_ocr_plate or payload.plate_number,
        "confidence": sighting.confidence,
        "vehicle_class": sighting.vehicle_class,
        "vehicle_color": sighting.vehicle_color,
        "timestamp": sighting.timestamp.isoformat(),
        "is_reconciled": reconciled,
        "reconciliation_reason": reason,
        "thumbnail": sighting.image_base64,
        "alert": alert
    }
    await ws_manager.broadcast(event)
    return {"status": "SUCCESS", "sighting_id": sighting.id, "reconciled": reconciled}

@router.post("/heartbeat")
async def ingest_heartbeat(payload: CameraHeartbeat, db: Session = Depends(get_db)):
    cam = db.query(CameraNode).filter(CameraNode.camera_id == payload.camera_id).first()
    if cam:
        cam.fps_current = payload.fps
        cam.last_heartbeat = datetime.utcnow()
        cam.is_active = True
        db.commit()
    return {"status": "ACK"}
