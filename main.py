import os
import cv2

from dotenv import load_dotenv
from datetime import datetime

from detector.detection import ProductDetector
from database.db import Database
from helpers.storage import generate_file_paths

load_dotenv()

EXPECTED_PRODUCTS = int(
    os.getenv("EXPECTED_PRODUCTS")
)

USERNAME = "putra"

detector = ProductDetector()

db = Database()


def main():

    start_time = datetime.now()

    image_path = "images/sample.jpg"

    original_path, result_path = (
        generate_file_paths()
    )

    #
    # Simpan original
    #
    image = cv2.imread(image_path)

    cv2.imwrite(
        original_path,
        image
    )

    #
    # YOLO detect
    #
    count, results = detector.detect(
        original_path
    )

    #
    # Status
    #
    status = (
        "OK"
        if count == EXPECTED_PRODUCTS
        else "KURANG"
    )

    #
    # Simpan result
    #
    plotted = results[0].plot()

    cv2.imwrite(
        result_path,
        plotted
    )

    #
    # Simpan DB
    #
    inspection_id = db.save_log(
        username=USERNAME,
        image_original=original_path,
        image_result=result_path,
        count=count,
        status=status
    )

    processing_time = (
        datetime.now() - start_time
    ).total_seconds()

    print("=" * 50)
    print(f"Inspection ID : {inspection_id}")
    print(f"Username      : {USERNAME}")
    print(f"Count         : {count}")
    print(f"Expected      : {EXPECTED_PRODUCTS}")
    print(f"Status        : {status}")
    print(f"Process Time  : {processing_time:.2f}s")
    print(f"Original      : {original_path}")
    print(f"Result        : {result_path}")
    print("=" * 50)

    db.close()


if __name__ == "__main__":
    main()