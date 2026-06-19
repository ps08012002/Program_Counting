from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Bottle Counting API",
    version="1.0.0",
    description="Internal API untuk deteksi dan perhitungan botol menggunakan YOLO"
)

app.include_router(router)


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": "bottle-counting-api",
        "version": "1.0.0"
    }