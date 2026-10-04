from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import csv
import io
from backend.app.database import get_db
from backend.app.models.watchlist import Watchlist

router = APIRouter()

@router.get("/")
def get_watchlist(db: Session = Depends(get_db)):
    return db.query(Watchlist).all()

@router.post("/upload_csv")
def upload_watchlist_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    added = 0
    for row in reader:
        plate = row.get("plate_number", "").upper().strip()
        if not plate:
            continue
        exists = db.query(Watchlist).filter(Watchlist.plate_number == plate).first()
        if not exists:
            w = Watchlist(
                plate_number=plate,
                case_reference=row.get("case_reference", "UNSPECIFIED-FIR"),
                crime_category=row.get("crime_category", "Suspicious Vehicle"),
                severity_level=row.get("severity_level", "HIGH")
            )
            db.add(w)
            added += 1
    db.commit()
    return {"status": "SUCCESS", "records_imported": added}
