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
