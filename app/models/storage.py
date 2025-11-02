"""This module defines the storage paths for the application."""
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
LATEX_DIR = DATA_DIR / "latex"
PDF_DIR = DATA_DIR / "pdf"


def ensure_dirs() -> None:
    """Ensures that all the data directories exist."""
    for d in (DATA_DIR, UPLOADS_DIR, PROCESSED_DIR, LATEX_DIR, PDF_DIR):
        d.mkdir(parents=True, exist_ok=True)


def path_for_upload(upload_id: str) -> Path:
    """Returns the path to an uploaded file."""
    return UPLOADS_DIR / f"{upload_id}"


def path_for_processed(processed_id: str) -> Path:
    """Returns the path to a processed file."""
    return PROCESSED_DIR / f"{processed_id}"


def path_for_latex(latex_id: str) -> Path:
    """Returns the path to a LaTeX file."""
    return LATEX_DIR / f"{latex_id}.tex"


def path_for_pdf(pdf_id: str) -> Path:
    """Returns the path to a PDF file."""
    return PDF_DIR / f"{pdf_id}.pdf"
