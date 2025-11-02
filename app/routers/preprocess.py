"""This module defines the API endpoints for preprocessing images."""

import uuid
from fastapi import APIRouter, HTTPException

from app.models.schemas import PreprocessOptions, PreprocessResponse
from app.models import storage
from app.services.image_preprocess import apply_preprocessing


router = APIRouter(prefix="/api", tags=["preprocess"])


@router.post("/preprocess/{upload_id}", response_model=PreprocessResponse)
def preprocess_image(upload_id: str, options: PreprocessOptions) -> PreprocessResponse:
    """Applies preprocessing to an uploaded image.

    Args:
        upload_id: The ID of the uploaded image to preprocess.
        options: The preprocessing options.

    Returns:
        A PreprocessResponse containing the processedId of the processed image.
    """
    storage.ensure_dirs()
    src = storage.path_for_upload(upload_id)
    if not src.exists():
        raise HTTPException(status_code=404, detail="uploadId not found")
    processed_id = str(uuid.uuid4())
    dst = storage.path_for_processed(processed_id)
    apply_preprocessing(src, dst, options)
    return PreprocessResponse(processedId=processed_id)
