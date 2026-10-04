from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.trajectory import TrajectoryReconstructionResponse
from backend.app.services.trajectory_service import TrajectoryService
from backend.app.models.audit_log import AuditLog

router = APIRouter()

@router.get("/track/{plate_number}", response_model=TrajectoryReconstructionResponse)
def get_vehicle_track(
    plate_number: str,
    operator_id: str = Query("OP-104", description="Badge ID of investigating officer"),
    db: Session = Depends(get_db)):
    clean_plate = plate_number.upper().strip()
    service = TrajectoryService(db)
    res = service.get_full_trajectory(clean_plate)

    log = AuditLog(
        operator_id=operator_id,
        action="QUERY_TRAJECTORY",
        target_plate=clean_plate,
        details=f"Retrieved {res.total_legs} route legs"
    )
    db.add(log)
    db.commit()
    return res
