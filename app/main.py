from pathlib import Path

from fastapi import FastAPI
from .routers import uploads, preprocess, convert, compile as compile_routes, status


app = FastAPI(title="LaTech FastAPI App")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(uploads.router)
app.include_router(preprocess.router)
app.include_router(convert.router)
app.include_router(compile_routes.router)
app.include_router(status.router)


if __name__ == "__main__":
    # Allows: python app/main.py (useful for quick local testing)
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


