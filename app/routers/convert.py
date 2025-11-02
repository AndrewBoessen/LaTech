"""This module defines the API endpoints for converting images to LaTeX."""

import uuid
from fastapi import APIRouter, HTTPException

from app.models.schemas import ConvertResponse
from app.models import storage
from app.services.ocr_to_latex import convert_image_to_latex


router = APIRouter(prefix="/api", tags=["convert"])


@router.post("/convert/{processed_id}", response_model=ConvertResponse)
def convert_to_latex(processed_id: str) -> ConvertResponse:
    """Converts a processed image to LaTeX.

    Args:
        processed_id: The ID of the processed image to convert.

    Returns:
        A ConvertResponse containing the latexId and the converted LaTeX code.
    """
    storage.ensure_dirs()
    src = storage.path_for_processed(processed_id)
    if not src.exists():
        raise HTTPException(status_code=404, detail="processedId not found")
    latex_id = str(uuid.uuid4())
    latex = convert_image_to_latex(src)
    latex_path = storage.path_for_latex(latex_id)
    latex_path.write_text(latex, encoding="utf-8")
    return ConvertResponse(latexId=latex_id, latex=latex)
