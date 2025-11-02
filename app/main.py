"""The main entrypoint for the LaTech FastAPI application."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import uploads, preprocess, convert, compile as compile_routes, status


app = FastAPI(title="LaTech FastAPI App")

# CORS configuration: allow frontend origins
_cors_env = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173")
_allowed_origins = [o.strip() for o in _cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    """A health check endpoint that returns the status of the application."""
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
