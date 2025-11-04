"""This module provides a function to convert an image to LaTeX using Gemini."""

import os
from pathlib import Path
from google import genai

# Configure the Gemini client
client = genai.Client()

# Set up the model
MODEL_NAME = "gemini-2.5-flash"
PROMPT = """Please convert the following image to a self-contained,\\
compilable LaTeX document, including a documentclass, necessary packages,\\
and begin/end document environments. The image contains mathematical equations and text."""


def convert_image_to_latex(image_path: Path) -> str:
    """Converts an image to LaTeX using the Gemini 2.5 Pro model.

    Args:
        image_path: The path to the image to convert.

    Returns:
        The converted LaTeX code.
    """
    try:
        file = client.files.upload(file=image_path)
        response = client.models.generate_content(
            model=MODEL_NAME, contents=[file, PROMPT]
        )
        return response.text
    except Exception as e:
        # Re-raise exceptions to be handled by the calling router
        raise RuntimeError(f"Failed to convert image to LaTeX: {e}") from e
