import uuid
from fastapi import APIRouter, HTTPException

from ..models.schemas import ConvertResponse
from ..models import storage
from ..services.ocr_to_latex import convert_image_to_latex


router = APIRouter(prefix="/api", tags=["convert"])


@router.post("/convert/{processed_id}", response_model=ConvertResponse)
def convert_to_latex(processed_id: str) -> ConvertResponse:
    storage.ensure_dirs()
    src = storage.path_for_processed(processed_id)
    if not src.exists():
        raise HTTPException(status_code=404, detail="processedId not found")
    latex_id = str(uuid.uuid4())
    latex = convert_image_to_latex(src)
    latex_path = storage.path_for_latex(latex_id)
    latex_path.write_text(latex, encoding="utf-8")
    return ConvertResponse(latexId=latex_id, latex=latex)


