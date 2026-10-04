import re
from typing import Optional, Tuple

class IndianPlateCorrector:
    CHAR_TO_NUM = {'O': '0', 'I': '1', 'L': '1', 'Z': '2', 'S': '5', 'G': '6', 'B': '8', 'D': '0', 'Q': '0'}
    NUM_TO_CHAR = {'0': 'O', '1': 'I', '2': 'Z', '5': 'S', '6': 'G', '8': 'B'}

    INDIAN_STATES = {
        "AN", "AP", "AR", "AS", "BR", "CH", "CG", "DD", "DL", "DN",
        "GA", "GJ", "HR", "HP", "JH", "JK", "KA", "KL", "LA", "LD",
        "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "PY", "RJ",
        "SK", "TN", "TS", "TR", "UP", "UK", "WB"
    }

    @classmethod
    def clean_text(cls, raw_text: str) -> str:
        return re.sub(r'[^A-Z0-9]', '', raw_text.upper())

    @classmethod
    def correct_standard_plate(cls, text: str) -> Optional[str]:
        if len(text) < 8 or len(text) > 11:
            return None

        chars = list(text)

        for i in (0, 1):
            if chars[i] in cls.NUM_TO_CHAR:
                chars[i] = cls.NUM_TO_CHAR[chars[i]]

        for i in (2, 3):
            if chars[i] in cls.CHAR_TO_NUM:
                chars[i] = cls.CHAR_TO_NUM[chars[i]]

        for i in range(len(chars) - 4, len(chars)):
            if chars[i] in cls.CHAR_TO_NUM:
                chars[i] = cls.CHAR_TO_NUM[chars[i]]

        for i in range(4, len(chars) - 4):
            if chars[i] in cls.NUM_TO_CHAR:
                chars[i] = cls.NUM_TO_CHAR[chars[i]]

        corrected = "".join(chars)
        regex = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}$'
        if re.match(regex, corrected):
            return corrected
        return None

    @classmethod
    def correct_bharat_series(cls, text: str) -> Optional[str]:
        if len(text) != 10:
            return None

        chars = list(text)
        for i in (0, 1):
            if chars[i] in cls.CHAR_TO_NUM:
                chars[i] = cls.CHAR_TO_NUM[chars[i]]

        chars[2] = 'B' if chars[2] in ('8', 'B') else chars[2]
        chars[3] = 'H'

        for i in range(4, 8):
            if chars[i] in cls.CHAR_TO_NUM:
                chars[i] = cls.CHAR_TO_NUM[chars[i]]

        for i in (8, 9):
            if chars[i] in cls.NUM_TO_CHAR:
                chars[i] = cls.NUM_TO_CHAR[chars[i]]

        corrected = "".join(chars)
        regex = r'^[0-9]{2}BH[0-9]{4}[A-Z]{1,2}$'
        if re.match(regex, corrected):
            return corrected
        return None

    @classmethod
    def disambiguate(cls, raw_ocr: str) -> Tuple[str, bool]:
        cleaned = cls.clean_text(raw_ocr)
        std = cls.correct_standard_plate(cleaned)
        if std:
            return std, True
        bh = cls.correct_bharat_series(cleaned)
        if bh:
            return bh, True
        return cleaned, False
