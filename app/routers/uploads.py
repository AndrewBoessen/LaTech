"""This module defines the API endpoints for uploading images."""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import UploadResponse
from app.models import storage


router = APIRouter(prefix="/api", tags=["uploads"])


@router.post("/uploads", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    """Uploads an image file.

    Args:
        file: The image file to upload.

    Returns:
        An UploadResponse containing the uploadId of the uploaded image.
    """
    storage.ensure_dirs()
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")
    upload_id = f"{uuid.uuid4()}_{file.filename}"
    dest = storage.path_for_upload(upload_id)
    dest.write_bytes(await file.read())
    return UploadResponse(uploadId=upload_id)
