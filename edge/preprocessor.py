import cv2
import numpy as np

class PlatePreprocessor:
    @staticmethod
    def deskew_and_enhance(crop: np.ndarray) -> np.ndarray:
        if crop is None or crop.size == 0:
            return crop

        target_h = 96
        h, w = crop.shape[:2]
        if h == 0 or w == 0:
            return crop
        target_w = int(w * (target_h / h))
        resized = cv2.resize(crop, (target_w, target_h), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        filtered = cv2.bilateralFilter(enhanced, d=7, sigmaColor=75, sigmaSpace=75)

        _, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) > 50:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            if abs(angle) > 2.0 and abs(angle) < 30.0:
                center = (target_w // 2, target_h // 2)
                rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
                deskewed = cv2.warpAffine(
                    filtered, rot_mat, (target_w, target_h),
                    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
                )
                return deskewed

        return filtered
