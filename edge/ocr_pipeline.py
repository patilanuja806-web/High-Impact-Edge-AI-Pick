import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
from edge.preprocessor import PlatePreprocessor
from edge.plate_corrector import IndianPlateCorrector

class AnprOcrPipeline:
    def __init__(self, use_gpu: bool = False):
        self.ocr = PaddleOCR(use_angle_cls=False, lang="en", show_log=False)
        self.preprocessor = PlatePreprocessor()

    def process_crop(self, plate_bgr: np.ndarray) -> dict:
        if plate_bgr is None or plate_bgr.size == 0:
            return {"raw_text": "", "clean_text": "", "confidence": 0.0, "is_valid": False}

        enhanced = self.preprocessor.deskew_and_enhance(plate_bgr)
        if len(enhanced.shape) == 2:
            enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        else:
            enhanced_bgr = enhanced

        results = self.ocr.ocr(enhanced_bgr, cls=False)
        if not results or not results[0]:
            return {"raw_text": "", "clean_text": "", "confidence": 0.0, "is_valid": False}

        extracted_words = []
        confidences = []

        try:
            for line in results[0]:
                extracted_words.append(line[1][0])
                confidences.append(float(line[1][1]))
        except Exception:
            pass

        raw_joined = "".join(extracted_words)
        mean_conf = float(np.mean(confidences)) if confidences else 0.0
        clean_plate, is_valid = IndianPlateCorrector.disambiguate(raw_joined)

        return {
            "raw_text": raw_joined,
            "clean_text": clean_plate,
            "confidence": round(mean_conf, 3),
            "is_valid": is_valid
        }
