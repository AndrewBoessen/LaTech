from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


app = FastAPI(title="LaTech FastAPI App")

# Serve static assets (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=FileResponse)
def read_root() -> FileResponse:
    """Serve the main HTML file."""
    return FileResponse(STATIC_DIR / "index.html")


class EchoRequest(BaseModel):
    message: str


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/echo")
def echo(payload: EchoRequest) -> dict:
    return {"echo": payload.message}


if __name__ == "__main__":
    # Allows: python app/main.py (useful for quick local testing)
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


