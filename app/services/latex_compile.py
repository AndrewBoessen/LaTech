"""This module provides a function to compile LaTeX source code to a PDF file."""

import subprocess
import shutil
from pathlib import Path


def compile_latex_to_pdf(latex_source_path: Path, pdf_out_path: Path) -> None:
    """Compiles a LaTeX source file to a PDF file using pdflatex.

    Args:
        latex_source_path: The path to the LaTeX source file.
        pdf_out_path: The path to write the PDF file to.

    Raises:
        RuntimeError: If the compilation fails.
    """
    latex_content = latex_source_path.read_text(encoding="utf-8")

    # Check if the content is a full document or just a fragment
    if "\\documentclass" not in latex_content:
        # Wrap the content in a minimal document structure
        latex_content = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
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
            encoding="utf-8",
        )
        # Move the generated PDF to the desired output path
        generated_pdf = pdf_out_path.parent / latex_source_path.with_suffix(".pdf").name
        shutil.move(generated_pdf, pdf_out_path)
    except subprocess.CalledProcessError as e:
        # The error message from pdflatex is in the stderr stream
        raise RuntimeError(f"LaTeX compilation failed: {e.stderr}") from e
    except FileNotFoundError as e:
        raise RuntimeError(
            "pdflatex command not found. Is LaTeX installed and in your PATH?"
        ) from e
