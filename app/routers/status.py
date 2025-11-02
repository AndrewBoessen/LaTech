"""This module defines the API endpoints for checking the status of a job."""

from fastapi import APIRouter

from app.models.schemas import StatusResponse


router = APIRouter(prefix="/api", tags=["status"])


@router.get("/status/{job_id}", response_model=StatusResponse)
def get_status(job_id: str) -> StatusResponse:
    """Gets the status of a job.

    Args:
        job_id: The ID of the job to get the status of.

    Returns:
        A StatusResponse containing the status of the job.
    """
    # Placeholder: always done
    return StatusResponse(state="done", progress=100)
