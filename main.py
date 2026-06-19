import os
import cv2

from dotenv import load_dotenv
from datetime import datetime

from detector.detection import ProductDetector
from database.db import Database
from helpers.storage import generate_file_paths

load_dotenv()

expected_products = os.getenv(
    "EXPECTED_PRODUCTS"
)

if not expected_products:
    raise RuntimeError(
        "EXPECTED_PRODUCTS not found in environment variables"
    )

EXPECTED_PRODUCTS = int(
    expected_products
)

detector = ProductDetector()
db = Database()


def process_image(
    image_path,
    username
):
    start_time = datetime.now()

    original_path, result_path = (
        generate_file_paths(
            username
        )
    )

    #
    # READ IMAGE
    #
    image = cv2.imread(
        image_path
    )

    if image is None:
        raise RuntimeError(
            f"Failed to read image: {image_path}"
        )

    #
    # SAVE ORIGINAL IMAGE
    #
    if not cv2.imwrite(
        original_path,
        image
    ):
        raise RuntimeError(
            "Failed to save original image"
        )

    #
    # YOLO DETECTION
    #
    count, results = detector.detect(
        original_path
    )

    #
    # STATUS
    #
    status = (
        "OK"
        if count == EXPECTED_PRODUCTS
        else "KURANG"
    )

    #
    # SAVE RESULT IMAGE
    #
    plotted = results[0].plot()

    if not cv2.imwrite(
        result_path,
        plotted
    ):
        raise RuntimeError(
            "Failed to save result image"
        )

    #
    # FILE SIZE
    #
    original_size = os.path.getsize(
        original_path
    )

    result_size = os.path.getsize(
        result_path
    )

    file_size_mb = round(
        (
            original_size +
            result_size
        ) / 1024 / 1024,
        2
    )

    #
    # PROCESSING TIME
    #
    processing_time = (
        datetime.now() - start_time
    ).total_seconds()

    #
    # SAVE DATABASE LOG
    #
    inspection_id = db.save_log(
        username=username,
        image_original=original_path,
        image_result=result_path,
        count=count,
        status=status,
        file_size_mb=file_size_mb,
        processing_time=processing_time
    )

    #
    # LOG
    #
    print("=" * 60)
    print(
        f"Inspection ID : {inspection_id}"
    )
    print(
        f"Username      : {username}"
    )
    print(
        f"File          : {os.path.basename(image_path)}"
    )
    print(
        f"Count         : {count}"
    )
    print(
        f"Expected      : {EXPECTED_PRODUCTS}"
    )
    print(
        f"Status        : {status}"
    )
    print(
        f"File Size     : {file_size_mb:.2f} MB"
    )
    print(
        f"Process Time  : {processing_time:.2f}s"
    )
    print(
        f"Original      : {original_path}"
    )
    print(
        f"Result        : {result_path}"
    )
    print("=" * 60)

    return {
        "success": True,
        "inspection_id": inspection_id,
        "username": username,
        "count": count,
        "expected": EXPECTED_PRODUCTS,
        "status": status,
        "file_size_mb": file_size_mb,
        "processing_time": processing_time,
        "image_original": original_path,
        "image_result": result_path
    }


if __name__ == "__main__":
    print(
        "Gunakan endpoint API /detect untuk menjalankan proses deteksi."
    )