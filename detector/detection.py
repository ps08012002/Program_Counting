import os

from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()


class ProductDetector:

    def __init__(self):

        self.model = YOLO(
            os.getenv("YOLO_MODEL")
        )

    def detect(self, image_path):

        results = self.model(
            image_path,
            conf=0.5
        )

        count = len(
            results[0].boxes
        )

        return count, results