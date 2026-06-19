import os
import tempfile

from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Header,
    HTTPException,
    Request
)

from main import process_image

load_dotenv()

#
# REQUIRED ENVIRONMENT VARIABLES
#

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError(
        "API_KEY not found in environment variables"
    )

MAX_FILE_SIZE_MB = os.getenv(
    "MAX_FILE_SIZE_MB"
)

if not MAX_FILE_SIZE_MB:
    raise RuntimeError(
        "MAX_FILE_SIZE_MB not found in environment variables"
    )

MAX_FILE_SIZE = (
    int(MAX_FILE_SIZE_MB)
    * 1024
    * 1024
)

ENABLE_IP_WHITELIST = (
    os.getenv(
        "ENABLE_IP_WHITELIST",
        "false"
    ).lower()
    == "true"
)

DASHBOARD_IP = os.getenv(
    "DASHBOARD_IP"
)

#
# ALLOWED FILE TYPES
#

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

router = APIRouter()


@router.post("/detect")
async def detect_image(
    request: Request,
    username: str = Form(...),
    file: UploadFile = File(...),
    x_api_key: str = Header(...)
):
    #
    # API KEY VALIDATION
    #
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    #
    # OPTIONAL IP WHITELIST
    #
    if ENABLE_IP_WHITELIST:

        if not DASHBOARD_IP:
            raise RuntimeError(
                "DASHBOARD_IP not configured"
            )

        client_ip = request.client.host

        if client_ip != DASHBOARD_IP:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    #
    # VALIDATE FILE EXTENSION
    #
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    temp_file = None

    try:

        #
        # READ FILE
        #
        content = await file.read()

        #
        # FILE SIZE LIMIT
        #
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File exceeds "
                    f"{MAX_FILE_SIZE_MB}MB limit"
                )
            )

        #
        # TEMP FILE
        #
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        )

        temp_file.close()

        with open(
            temp_file.name,
            "wb"
        ) as f:
            f.write(content)

        #
        # PROCESS IMAGE
        #
        result = process_image(
            image_path=temp_file.name,
            username=username
        )

        return result

    except HTTPException:
        raise

    except Exception as e:

        print(
            f"[ERROR] detect_image: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    finally:

        if (
            temp_file
            and
            os.path.exists(temp_file.name)
        ):
            try:
                os.remove(temp_file.name)

            except Exception as e:

                print(
                    "[WARNING] "
                    f"Failed to remove temp file: {e}"
                )