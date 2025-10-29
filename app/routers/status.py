from fastapi import APIRouter

from ..models.schemas import StatusResponse


router = APIRouter(prefix="/api", tags=["status"])


@router.get("/status/{job_id}", response_model=StatusResponse)
def get_status(job_id: str) -> StatusResponse:
    # Placeholder: always done
    return StatusResponse(state="done", progress=100)


