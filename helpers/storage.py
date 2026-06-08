import os

from datetime import datetime


def create_storage_folder():

    now = datetime.now()

    base_folder = os.path.join(
        "storage",
        str(now.year),
        f"{now.month:02}",
        f"{now.day:02}"
    )

    original_folder = os.path.join(
        base_folder,
        "original"
    )

    result_folder = os.path.join(
        base_folder,
        "result"
    )

    os.makedirs(
        original_folder,
        exist_ok=True
    )

    os.makedirs(
        result_folder,
        exist_ok=True
    )

    return original_folder, result_folder


def generate_file_paths():

    original_folder, result_folder = (
        create_storage_folder()
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    original_filename = (
        f"{timestamp}_original.jpg"
    )

    result_filename = (
        f"{timestamp}_result.jpg"
    )

    original_path = os.path.join(
        original_folder,
        original_filename
    )

    result_path = os.path.join(
        result_folder,
        result_filename
    )

    return original_path, result_path