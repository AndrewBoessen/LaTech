"""This module defines the API endpoints for uploading images."""

import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import job as job_model
from app.models.schemas import JobResponse
from app.models import storage


router = APIRouter(prefix="/api", tags=["uploads"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/uploads", response_model=JobResponse)
async def upload_image(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> JobResponse:
    """Uploads an image file and creates a new job.

    Args:
        file: The image file to upload.
        db: The database session.

    Returns:
        A JobResponse containing the job_id of the new job.
    """
    storage.ensure_dirs()
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")
    upload_id = f"{uuid.uuid4()}_{file.filename}"
    dest = storage.path_for_upload(upload_id)
    dest.write_bytes(await file.read())
    job_id = str(uuid.uuid4())
    job = job_model.Job(
        job_id=job_id, status="uploaded", upload_id=upload_id, name=file.filename
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return JobResponse(job_id=job_id)


@router.get("/uploads/{job_id}/image")
def get_uploaded_image(job_id: str, db: Session = Depends(get_db)):
    """Returns the uploaded image for a job.

    Args:
        job_id: The ID of the job.
        db: The database session.

    Returns:
        A FileResponse containing the uploaded image.
    """
    from fastapi.responses import FileResponse

    storage.ensure_dirs()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="jobId not found")

    path = storage.path_for_upload(job.upload_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path)
