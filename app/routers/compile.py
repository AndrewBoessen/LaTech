"""This module defines the API endpoints for compiling LaTeX to PDF."""

import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import job as job_model
from app.models.schemas import JobResponse
from app.models import storage
from app.services.latex_compile import compile_latex_to_pdf


router = APIRouter(prefix="/api", tags=["compile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_compilation(job_id: str):
    """Runs the LaTeX to PDF compilation.

    Args:
        job_id: The ID of the job.
    """
    db = SessionLocal()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        db.close()
        return

    job.status = "compiling"
    db.commit()

    latex_path = storage.path_for_latex(job.latex_id)
    if not latex_path.exists():
        job.status = "failed"
        db.commit()
        db.close()
        return
    pdf_id = str(uuid.uuid4())
    pdf_path = storage.path_for_pdf(pdf_id)
    success, _ = compile_latex_to_pdf(latex_path, pdf_path)
    if not success:
        job.status = "failed"
        db.commit()
        db.close()
        return
    job.pdf_id = pdf_id
    job.status = "complete"
    db.commit()
    db.close()


@router.post("/compile/{job_id}", response_model=JobResponse)
def compile_latex(
    job_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> JobResponse:
    """Compiles LaTeX source code to a PDF file.

    Args:
        job_id: The ID of the job.
        background_tasks: The background tasks manager.
        db: The database session.

    Returns:
        A JobResponse containing the job_id of the job.
    """
    storage.ensure_dirs()
    job = db.query(job_model.Job).filter(job_model.Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="jobId not found")
    background_tasks.add_task(run_compilation, job_id)
    return JobResponse(job_id=job_id)


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