"""This module provides a function to convert an image to LaTeX using Gemini."""

import os
import re
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
        if not response or not response.text:
            raise ValueError("Invalid or empty response from the model.")

        # Check for a markdown embedded latex code. Extract this code and then return if it exists
        match = re.search(r"```latex(.*)```", response.text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response.text
    except ValueError as e:
        # Re-raise exceptions to be handled by the calling router
        raise RuntimeError(f"Failed to convert image to LaTeX: {e}") from e
