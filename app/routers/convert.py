"""This module defines the API endpoints for converting images to LaTeX."""

import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import job as job_model
from app.models.schemas import JobResponse
from app.models import storage
from app.services.ocr_to_latex import convert_image_to_latex


router = APIRouter(prefix="/api", tags=["convert"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_conversion(job_id: str):
    """Runs the image to LaTeX conversion.

    Args:
        job_id: The ID of the job.
    """
    db = SessionLocal()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        db.close()
        return

    job.status = "converting"
    db.commit()

    src = storage.path_for_processed(job.processed_id)
    if not src.exists():
        job.status = "failed"
        db.commit()
        db.close()
        return
    latex_id = str(uuid.uuid4())
    latex = convert_image_to_latex(src)
    latex_path = storage.path_for_latex(latex_id)
    latex_path.write_text(latex, encoding="utf-8")
    job.latex_id = latex_id
    job.status = "compiling"
    db.commit()
    db.close()


@router.post("/convert/{job_id}", response_model=JobResponse)
def convert_to_latex(
    job_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> JobResponse:
    """Converts a processed image to LaTeX.

    Args:
        job_id: The ID of the job.
        background_tasks: The background tasks manager.
        db: The database session.

    Returns:
        A JobResponse containing the job_id of the job.
    """
    storage.ensure_dirs()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="jobId not found")
    background_tasks.add_task(run_conversion, job_id)
    return JobResponse(job_id=job_id)