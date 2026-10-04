import os
import cv2
import time
import base64
import requests
import numpy as np
from ultralytics import YOLO
from edge.ocr_pipeline import AnprOcrPipeline
from edge.tracker import MultiFrameVoter

CAMERA_ID = os.getenv("CAMERA_ID", "CAM_JNC_A")
VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", "test_assets/videos/camera_a_sector18.mp4")
BACKEND_INGEST_URL = os.getenv("BACKEND_INGEST_URL", "http://localhost:8000/api/v1/ingest/sighting")
HEARTBEAT_URL = os.getenv("BACKEND_HEARTBEAT_URL", "http://localhost:8000/api/v1/ingest/heartbeat")

def encode_thumbnail(crop: np.ndarray) -> str:
    if crop is None or crop.size == 0:
        return ""
    h, w = crop.shape[:2]
    new_w = 160
    new_h = int(h * (160 / w))
    thumb = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_AREA)
    _, buffer = cv2.imencode(".jpg", thumb, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return base64.b64encode(buffer).decode("utf-8")

def run_node():
    print(f"[*] Starting Edge Node [{CAMERA_ID}] connected to: {VIDEO_SOURCE}")
    model = YOLO("yolov8n.pt")
    ocr_pipeline = AnprOcrPipeline(use_gpu=False)
    voter = MultiFrameVoter(min_votes=2, max_history=10)

    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"[!] Error: Could not open video source {VIDEO_SOURCE}")
        return

    frame_count = 0
    fps_start_time = time.time()
    last_heartbeat_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_count += 1
        results = model.track(frame, persist=True, classes=[2, 3, 5, 7], verbose=False)
        
        if results and results[0].boxes and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, track_id, cls_id in zip(boxes, track_ids, classes):
                x1, y1, x2, y2 = map(int, box)
                w, h = x2 - x1, y2 - y1
                
                plate_y1 = int(y1 + 0.65 * h)
                plate_y2 = int(y1 + 0.95 * h)
                plate_x1 = int(x1 + 0.20 * w)
                plate_x2 = int(x1 + 0.80 * w)

                plate_crop = frame[max(0, plate_y1):min(frame.shape[0], plate_y2),
                                   max(0, plate_x1):min(frame.shape[1], plate_x2)]

                if plate_crop.shape[0] < 15 or plate_crop.shape[1] < 40:
                    continue

                ocr_result = ocr_pipeline.process_crop(plate_crop)
                finalized = voter.add_observation(track_id, ocr_result)

                if finalized:
                    thumb_b64 = encode_thumbnail(plate_crop)
                    payload = {
                        "camera_id": CAMERA_ID,
                        "plate_number": finalized["plate_number"],
                        "raw_ocr_plate": ocr_result["raw_text"],
                        "confidence": finalized["confidence"],
                        "vehicle_class": "Car" if cls_id == 2 else "Heavy Vehicle",
                        "vehicle_color": "White",
                        "image_base64": thumb_b64
                    }
                    try:
                        requests.post(BACKEND_INGEST_URL, json=payload, timeout=0.8)
                        print(f"[+] EMITTED: {finalized['plate_number']} (Conf: {finalized['confidence']})")
                    except Exception as e:
                        print(f"[-] Backend unreachable: {e}")

        if time.time() - last_heartbeat_time >= 5.0:
            current_fps = frame_count / (time.time() - fps_start_time)
            try:
                requests.post(HEARTBEAT_URL, json={"camera_id": CAMERA_ID, "fps": round(current_fps, 1), "status": "ONLINE", "bandwidth_kbps": 1.8}, timeout=0.5)
            except Exception:
                pass
            last_heartbeat_time = time.time()

    cap.release()

if __name__ == "__main__":
    run_node()
