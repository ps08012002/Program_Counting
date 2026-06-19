import os

from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()


class ProductDetector:

    def __init__(self):

        model_path = os.getenv(
            "YOLO_MODEL"
        )

        if not model_path:
            raise RuntimeError(
                "YOLO_MODEL not found in environment variables"
            )

        if not os.path.exists(
            model_path
        ):
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        confidence = os.getenv(
            "YOLO_CONFIDENCE"
        )

        if not confidence:
            raise RuntimeError(
                "YOLO_CONFIDENCE not found in environment variables"
            )

        self.confidence = float(
            confidence
        )

        self.model = YOLO(
            model_path
        )

        print(
            f"[INFO] YOLO model loaded: {model_path}"
        )

    def detect(
        self,
        image_path
    ):

        try:

            results = self.model(
                image_path,
                conf=self.confidence
            )

            count = len(
                results[0].boxes
            )

            return count, results

        except Exception as e:

            raise RuntimeError(
                f"YOLO detection failed: {e}"
            )