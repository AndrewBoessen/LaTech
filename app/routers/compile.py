"""This module defines the API endpoints for compiling LaTeX to PDF."""
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

from ..models.schemas import CompileRequest, CompileResponse
from ..models import storage
from ..services.latex_compile import compile_latex_to_pdf


router = APIRouter(prefix="/api", tags=["compile"])


@router.post("/compile", response_model=CompileResponse)
def compile_latex(body: CompileRequest) -> CompileResponse:
    """Compiles LaTeX source code to a PDF file.

    Args:
        body: The request body, containing either LaTeX source code or a latexId.

    Returns:
        A CompileResponse containing the pdfId of the compiled PDF.
    """
    storage.ensure_dirs()
    if not body.latex and not body.latexId:
        raise HTTPException(status_code=400, detail="Provide latex or latexId")

    if body.latexId:
        latex_path = storage.path_for_latex(body.latexId)
        if not latex_path.exists():
            raise HTTPException(status_code=404, detail="latexId not found")
    else:
        latex_id = str(uuid.uuid4())
        latex_path = storage.path_for_latex(latex_id)
        latex_path.write_text(body.latex or "", encoding="utf-8")

    pdf_id = str(uuid.uuid4())
    pdf_path = storage.path_for_pdf(pdf_id)
    success, error_message = compile_latex_to_pdf(latex_path, pdf_path)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to compile LaTeX: {error_message}")
    return CompileResponse(pdfId=pdf_id)


@router.get("/latex/{latex_id}")
def get_latex(latex_id: str):
    """Retrieves a LaTeX source file.

    Args:
        latex_id: The ID of the LaTeX source file to retrieve.

    Returns:
        A PlainTextResponse containing the LaTeX source code.
    """
    storage.ensure_dirs()
    latex_path = storage.path_for_latex(latex_id)
    if not latex_path.exists():
        raise HTTPException(status_code=404, detail="latexId not found")
    return PlainTextResponse(latex_path.read_text(encoding="utf-8"))


@router.get("/pdf/{pdf_id}")
def get_pdf(pdf_id: str):
    """Retrieves a compiled PDF file.

    Args:
        pdf_id: The ID of the PDF file to retrieve.

    Returns:
        A FileResponse containing the PDF file.
    """
    storage.ensure_dirs()
    pdf_path = storage.path_for_pdf(pdf_id)
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="pdfId not found")
    return FileResponse(pdf_path, media_type="application/pdf")
