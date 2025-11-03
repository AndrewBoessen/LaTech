"""This module defines the API endpoints for preprocessing images."""

import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import job as job_model
from app.models.schemas import PreprocessOptions, JobResponse
from app.models import storage
from app.services.image_preprocess import apply_preprocessing


router = APIRouter(prefix="/api", tags=["preprocess"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_preprocessing(job_id: str, options: PreprocessOptions):
    """Runs the image preprocessing.

    Args:
        job_id: The ID of the job.
        options: The preprocessing options.
    """
    db = SessionLocal()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        db.close()
        return

    job.status = "preprocessing"
    db.commit()

    src = storage.path_for_upload(job.upload_id)
    if not src.exists():
        job.status = "failed"
        db.commit()
        db.close()
        return
    processed_id = str(uuid.uuid4())
    dst = storage.path_for_processed(processed_id)
    apply_preprocessing(src, dst, options)
    job.processed_id = processed_id
    job.status = "ready to convert"
    db.commit()
    db.close()


@router.post("/preprocess/{job_id}", response_model=JobResponse)
def preprocess_image(
    job_id: str,
    body: PreprocessOptions,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> JobResponse:
    """Applies preprocessing to an uploaded image.

    Args:
        job_id: The ID of the job.
        body: The request body, containing the preprocessing options.
        background_tasks: The background tasks manager.
        db: The database session.

    Returns:
        A JobResponse containing the job_id of the job.
    """
    storage.ensure_dirs()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="jobId not found")
    background_tasks.add_task(run_preprocessing, job_id, body)
    return JobResponse(job_id=job_id)
