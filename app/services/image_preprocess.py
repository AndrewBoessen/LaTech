"""This module provides a function for applying preprocessing to an image."""

from pathlib import Path

from models.schemas import PreprocessOptions


def apply_preprocessing(
    src_path: Path, dst_path: Path, options: PreprocessOptions
) -> None:
    """Applies preprocessing to an image.

    Args:
        src_path: The path to the source image.
        dst_path: The path to write the preprocessed image to.
        options: The preprocessing options.
    """
    # Placeholder: copy file without modification for now
    dst_path.write_bytes(src_path.read_bytes())
