import time
import requests
from datetime import datetime, timedelta

BACKEND_BASE = "http://localhost:8000/api/v1"

def trigger_demo_sequence():
    print("[*] Starting NetraGati Scripted Demo Sequence...")

    watchlist_target = {
        "plate_number": "DL01AB1234",
        "case_reference": "FIR-402/2026-NZ",
        "crime_category": "Hit-and-Run / Red Light Collision",
        "severity_level": "CRITICAL"
    }
    try:
        requests.post(f"{BACKEND_BASE}/watchlist/upload_csv", files={
            'file': ('watchlist.csv', "plate_number,case_reference,crime_category,severity_level\nDL01AB1234,FIR-402/2026-NZ,Hit-and-Run,CRITICAL")
        })
        print("[+] Seeded Hotlist Target: DL01AB1234")
    except Exception as e:
        print(f"[-] Could not seed hotlist: {e}")

    now = datetime.utcnow()

    # Event 1: Sector 18 (CAM_JNC_A)
    t1 = now - timedelta(minutes=6)
    e1 = {
        "camera_id": "CAM_JNC_A",
        "plate_number": "DL01AB1234",
        "raw_ocr_plate": "DL01AB1234",
        "confidence": 0.96,
        "vehicle_class": "Car",
        "vehicle_color": "White",
        "timestamp": t1.isoformat()
    }
    requests.post(f"{BACKEND_BASE}/ingest/sighting", json=e1)
    print("[+] Leg 1 Recorded: CAM_JNC_A (Sector 18) -> DL01AB1234")
    time.sleep(1)

    # Event 2: Golf Course (CAM_JNC_B) with blurred read
    t2 = now - timedelta(minutes=4)
    e2 = {
        "camera_id": "CAM_JNC_B",
        "plate_number": "DL01AB1284",
        "raw_ocr_plate": "DLO1AB1284",
        "confidence": 0.81,
        "vehicle_class": "Car",
        "vehicle_color": "White",
        "timestamp": t2.isoformat()
    }
    requests.post(f"{BACKEND_BASE}/ingest/sighting", json=e2)
    print("[+] Leg 2 Recorded: CAM_JNC_B (Golf Course) -> DL01AB1284 (Fuzzy Match Triggered)")
    time.sleep(1)

    # Event 3: Metro Interchange Toll (CAM_JNC_C)
    t3 = now - timedelta(minutes=1)
    e3 = {
        "camera_id": "CAM_JNC_C",
        "plate_number": "DL01AB1234",
        "raw_ocr_plate": "DL01AB1234",
        "confidence": 0.95,
        "vehicle_class": "Car",
        "vehicle_color": "White",
        "timestamp": t3.isoformat()
    }
    requests.post(f"{BACKEND_BASE}/ingest/sighting", json=e3)
    print("[+] Leg 3 Recorded: CAM_JNC_C (Interchange Toll) -> DL01AB1234")
    
    print("\n[✓] Demo Scenario Seeded Successfully.")
    print("    Action: In the web UI, search plate 'DL01AB1234' to render the complete route,")
    print("    view the fuzzy reconciliation card, and inspect downstream intercept predictions.")

if __name__ == "__main__":
    trigger_demo_sequence()
