"""This module provides a function to compile LaTeX source code to a PDF file."""

from pathlib import Path
from pylatex import Document, NoEscape


def compile_latex_to_pdf(
    latex_source_path: Path, pdf_out_path: Path
) -> tuple[bool, str | None]:
    """Compiles a LaTeX source file to a PDF file.

    Args:
        latex_source_path: The path to the LaTeX source file.
        pdf_out_path: The path to write the PDF file to.

    Returns:
        A tuple containing a boolean indicating success or failure, and an
        error message if the compilation failed.
    """
    latex_content = latex_source_path.read_text(encoding="utf-8")

    # Create a new document
    doc = Document()

    # Add the LaTeX content
    doc.append(NoEscape(latex_content))

    # Compile the document
    try:
        doc.generate_pdf(str(pdf_out_path.with_suffix("")), clean_tex=False)
        return (True, None)
    except Exception as e:
        # Catching a broad exception because pylatex can raise a variety of
        # exceptions during compilation, and it's not always clear which one
        # will be raised.
        return (False, str(e))
