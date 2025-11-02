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


class UploadResponse(BaseModel):
    """The response model for an image upload."""

    uploadId: str


class PreprocessResponse(BaseModel):
    """The response model for a preprocessing request."""

    processedId: str


class ConvertResponse(BaseModel):
    """The response model for a conversion request."""

    latexId: str
    latex: str


class CompileRequest(BaseModel):
    """The request model for a compilation request."""

    latex: Optional[str] = None
    latexId: Optional[str] = None


class CompileResponse(BaseModel):
    """The response model for a compilation request."""

    pdfId: str


class StatusResponse(BaseModel):
    """The response model for a status request."""

    state: str
    progress: int
    error: Optional[str] = None
