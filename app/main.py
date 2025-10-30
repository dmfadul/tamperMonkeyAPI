import json
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Response, Request, status
from app.config import CORS_ALLOW_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS

app = FastAPI()
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="static")

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


@app.put("/raw/data/", status_code=status.HTTP_204_NO_CONTENT)
async def put_data_raw(request: Request):
    """
    Replace payload.json with the request body (must be JSON).
    Always saves it with indentation for readability.
    Returns 204 No Content on success.
    """
    file_path = DATA_DIR / "payload.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Parse body as JSON
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # Save prettified JSON
    body = json.dumps(data, ensure_ascii=False, indent=2)
    tmp = file_path.with_suffix(".tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.replace(file_path)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
