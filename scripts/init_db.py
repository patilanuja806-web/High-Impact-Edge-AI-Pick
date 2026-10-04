import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.camera import CameraNode
from backend.app.models.watchlist import Watchlist
from backend.app.models.sighting import VehicleSighting
from backend.app.models.vehicle_track import VehicleTrajectorySegment
from backend.app.models.audit_log import AuditLog

def init():
    print("[*] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(CameraNode).count() == 0:
        print("[*] Seeding default camera topology...")
        sample_cameras = [
            CameraNode(camera_id="CAM_JNC_A", name="Sector 18 Crossing", junction_code="JNC_A", latitude=28.5701, longitude=77.3218),
            CameraNode(camera_id="CAM_JNC_B", name="Golf Course Road", junction_code="JNC_B", latitude=28.5645, longitude=77.3340),
            CameraNode(camera_id="CAM_JNC_C", name="Metro Interchange Toll", junction_code="JNC_C", latitude=28.5580, longitude=77.3485),
            CameraNode(camera_id="CAM_JNC_D", name="Expressway North Exit", junction_code="JNC_D", latitude=28.5490, longitude=77.3620)
        ]
        db.add_all(sample_cameras)

        watchlist_seed = Watchlist(
            plate_number="DL01AB1234",
            case_reference="FIR-402/2026-NZ",
            crime_category="Hit-and-Run / Major Collision",
            severity_level="CRITICAL"
        )
        db.add(watchlist_seed)
        db.commit()
        print("[+] Topology and initial critical watchlist seeded.")
    else:
        print("[*] Database tables already populated.")
    db.close()

if __name__ == "__main__":
    init()
