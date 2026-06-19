import os
import re

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

STORAGE_PATH = os.getenv(
    "STORAGE_PATH"
)

if not STORAGE_PATH:
    raise RuntimeError(
        "STORAGE_PATH not found in environment variables"
    )


def create_storage_folder():

    now = datetime.now()

    base_folder = os.path.join(
        STORAGE_PATH,
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


def generate_file_paths(
    username
):

    original_folder, result_folder = (
        create_storage_folder()
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    safe_username = re.sub(
        r"[^a-zA-Z0-9_-]",
        "",
        username.strip().lower()
    )

    original_filename = (
        f"{timestamp}_{safe_username}_original.jpg"
    )

    result_filename = (
        f"{timestamp}_{safe_username}_result.jpg"
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