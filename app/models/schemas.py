"""This module defines the Pydantic schemas for the API.

These schemas are used for request and response validation.
"""

from typing import Optional
from pydantic import BaseModel


class PreprocessResize(BaseModel):
    """Defines the resize options for preprocessing."""

    width: int
    height: int


class PreprocessOptions(BaseModel):
    """Defines the options for preprocessing an image."""

    grayscale: bool = True
    denoise: bool = False
    threshold: Optional[int] = None
    resize: Optional[PreprocessResize] = None
    adaptive_threshold: bool = False





class StatusResponse(BaseModel):
    """The response model for a status request."""

    state: str
    progress: int
    error: Optional[str] = None


class Job(BaseModel):
    """Defines a job for the pipeline."""

    job_id: str
    name: Optional[str] = None
    status: str
    upload_id: Optional[str] = None
    processed_id: Optional[str] = None
    latex_id: Optional[str] = None
    pdf_id: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        orm_mode = True


class JobCreate(BaseModel):
    """Defines the request for creating a job."""

    upload_id: str
    options: PreprocessOptions


class JobResponse(BaseModel):
    """The response model for a job creation request."""

    job_id: str
