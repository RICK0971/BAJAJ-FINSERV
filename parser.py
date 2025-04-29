import pytesseract
import cv2
import numpy as np
import tempfile
import re
from utils import is_out_of_range
from typing import List, Dict, Any

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_lab_tests(image_bytes: bytes) -> List[Dict[str, Any]]:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        image = cv2.imread(tmp_path)
        if image is None:
            raise ValueError("Failed to read image")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh)

        print("=== OCR Output ===")
        print(text)

        results = []
        lines = text.split("\n")
        for line in lines:
            if not line.strip():
                continue
                
            print(f"Processing line: {line}")
            # More flexible regex pattern
            match = re.search(r"([A-Za-z0-9 \(\)\-]+)\s+(\d+\.?\d*)\s*([\d\.]+\s*-\s*[\d\.]+)\s*([a-zA-Z/%]+)?", line)
            if match:
                test_name = match.group(1).strip()
                test_value = match.group(2).strip()
                ref_range = match.group(3).strip()
                unit = match.group(4).strip() if match.group(4) else ""
                out_of_range = is_out_of_range(test_value, ref_range)
                results.append({
                    "test_name": test_name,
                    "test_value": test_value,
                    "bio_reference_range": ref_range,
                    "test_unit": unit,
                    "lab_test_out_of_range": out_of_range
                })
        return results
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise

