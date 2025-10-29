import uuid
from fastapi import APIRouter, HTTPException

from ..models.schemas import PreprocessOptions, PreprocessResponse
from ..models import storage
from ..services.image_preprocess import apply_preprocessing


router = APIRouter(prefix="/api", tags=["preprocess"])


@router.post("/preprocess/{upload_id}", response_model=PreprocessResponse)
def preprocess_image(upload_id: str, options: PreprocessOptions) -> PreprocessResponse:
    storage.ensure_dirs()
    src = storage.path_for_upload(upload_id)
    if not src.exists():
        raise HTTPException(status_code=404, detail="uploadId not found")
    processed_id = str(uuid.uuid4())
    dst = storage.path_for_processed(processed_id)
    apply_preprocessing(src, dst, options)
    return PreprocessResponse(processedId=processed_id)


