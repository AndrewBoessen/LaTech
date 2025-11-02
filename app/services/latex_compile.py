"""This module provides a function to compile LaTeX source code to a PDF file."""

import subprocess
import shutil
from pathlib import Path


def compile_latex_to_pdf(
    latex_source_path: Path, pdf_out_path: Path
) -> tuple[bool, str | None]:
    """Compiles a LaTeX source file to a PDF file using pdflatex.

    Args:
        latex_source_path: The path to the LaTeX source file.
        pdf_out_path: The path to write the PDF file to.

    Returns:
        A tuple containing a boolean indicating success or failure, and an
        error message if the compilation failed.
    """
    latex_content = latex_source_path.read_text(encoding="utf-8")

    # Check if the content is a full document or just a fragment
    if "\\documentclass" not in latex_content:
        # Wrap the content in a minimal document structure
        latex_content = f"""
\\documentclass{{article}}
\\begin{{document}}
{latex_content}
\\end{{document}}
"""
        latex_source_path.write_text(latex_content, encoding="utf-8")

    command = [
        "pdflatex",
        "-output-directory",
        str(pdf_out_path.parent),
        str(latex_source_path),
    ]

    try:
        # The `capture_output=True` argument captures the stdout and stderr streams,
        # and `text=True` decodes them as text.
        # The `check=True` argument raises a `CalledProcessError` if the command
        # returns a non-zero exit code.
        subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        # Move the generated PDF to the desired output path
        generated_pdf = pdf_out_path.parent / latex_source_path.with_suffix(".pdf").name
        shutil.move(generated_pdf, pdf_out_path)
        return (True, None)
    except subprocess.CalledProcessError as e:
        # The error message from pdflatex is in the stderr stream
        return (False, e.stderr)
    except FileNotFoundError:
        return (
            False,
            "pdflatex command not found. Is LaTeX installed and in your PATH?",
        )
