import os
import requests
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.watchlist import Watchlist

class WatchlistAlertManager:
    @staticmethod
    def check_and_alert(plate: str, camera_name: str, db: Session) -> Optional[dict]:
        target = db.query(Watchlist).filter(Watchlist.plate_number == plate).first()
        if not target:
            return None

        alert_payload = {
            "type": "WATCHLIST_MATCH",
            "plate_number": target.plate_number,
            "case_ref": target.case_reference,
            "crime_category": target.crime_category,
            "severity": target.severity_level,
            "camera": camera_name
        }

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = (
                f"🚨 *NETRAGATI WATCHLIST INTERCEPT ALERT*\n\n"
                f"*Plate:* `{target.plate_number}`\n"
                f"*Case:* {target.case_reference}\n"
                f"*Crime:* {target.crime_category}\n"
                f"*Location:* {camera_name}\n"
                f"*Severity:* {target.severity_level}"
            )
            try:
                requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"},
                    timeout=1.5
                )
            except Exception:
                pass

        return alert_payload
