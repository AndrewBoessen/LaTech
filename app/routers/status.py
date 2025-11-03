"""This module defines the API endpoints for checking the status of a job."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import job as job_model
from app.models.schemas import Job


router = APIRouter(prefix="/api", tags=["status"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/status/{job_id}", response_model=Job)
def get_status(job_id: str, db: Session = Depends(get_db)) -> Job:
    """Gets the status of a job.

    Args:
        job_id: The ID of the job to get the status of.
        db: The database session.

    Returns:
        A Job containing the status of the job.
    """
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/jobs", response_model=List[Job])
def get_jobs(db: Session = Depends(get_db)) -> List[Job]:
    """Gets all jobs.

    Args:
        db: The database session.

    Returns:
        A list of all jobs.
    """
    return db.query(job_model.Job).all()
