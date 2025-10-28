from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Response
from app.config import CORS_ALLOW_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,  # Adjust as needed for security
    allow_credentials=False,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
    expose_headers=["Content-Type"],
)

BASE_DIR = Path(__file__).parent
STORE_DIR = BASE_DIR / "storage"
DATA_DIR = STORE_DIR / "data"


@app.get("/services/index/")
def root():
    return {"ok": True, "service": "gistlike-raw", "endpoints": ["/raw/data/"]}


@app.get("/raw/data/")
def get_data_raw():
    file_path = DATA_DIR / "payload.json"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    mime = "text/plain; charset=utf-8"
    content = file_path.read_bytes()
    headers = {"Cache-Control": "no-store"}

    return Response(content=content, media_type=mime, headers=headers)
