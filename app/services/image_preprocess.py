"""This module provides a function for applying preprocessing to an image."""

from pathlib import Path
import cv2

from app.models.schemas import PreprocessOptions


from typing import Optional, Any
import numpy as np

def apply_preprocessing(
    src_path: Path, options: PreprocessOptions, dst_path: Optional[Path] = None
) -> Optional[np.ndarray]:
    """Applies preprocessing to an image.

    Args:
        src_path: The path to the source image.
        options: The preprocessing options.
        dst_path: The path to write the preprocessed image to. If None, returns the image.

    Returns:
        The preprocessed image as a numpy array if dst_path is None, else None.
    """
    # 1. Load the image
    image = cv2.imread(str(src_path))
    if image is None:
        raise FileNotFoundError(f"Could not read image from {src_path}")

    # 2. Apply Grayscale (if requested OR needed for thresholding)
    # We convert to grayscale if 'grayscale' is true OR if 'threshold'
    # is set, as thresholding requires a single-channel image.
    is_gray = False
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        is_gray = True

    if options.grayscale or (options.threshold is not None) or options.adaptive_threshold:
        if not is_gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        is_gray = True

    # 3. Apply Denoising (if requested)
    # This respects the 'denoise: bool = False' default in the schema.
    if options.denoise:
        if is_gray:
            image = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
        else:  # Color denoising
            image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    # 4. Apply Thresholding (if requested)
    if options.adaptive_threshold and is_gray:
        # Adaptive thresholding for "scanner-like" look
        image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    elif options.threshold is not None:
        # Simple binary threshold
        # Image is guaranteed to be grayscale from step 2.
        _, image = cv2.threshold(image, options.threshold, 255, cv2.THRESH_BINARY)

    # 5. Apply Resize
    if options.resize is not None:
        # 5a. Explicit resize requested (from PreprocessResize)
        # This will stretch/squash the image to the exact dimensions.
        target_size = (options.resize.width, options.resize.height)
        orig_size = (image.shape[1], image.shape[0])  # (w, h)

        if target_size != orig_size:
            # Use INTER_CUBIC (better for upscaling) or INTER_AREA (better for downscaling)
            if target_size[0] > orig_size[0] or target_size[1] > orig_size[1]:
                interpolation = cv2.INTER_CUBIC
            else:
                interpolation = cv2.INTER_AREA

            image = cv2.resize(image, target_size, interpolation=interpolation)
    else:
        # 5b. No explicit resize. Use "reasonable defaults" (from prompt)
        # A good default for OCR is to ensure images are not too small.
        # We will upscale images with a width < 1000px, preserving aspect ratio.
        MIN_WIDTH = 1000
        orig_h, orig_w = image.shape[:2]

        if orig_w < MIN_WIDTH:
            # Upscale, preserving aspect ratio
            ratio = MIN_WIDTH / float(orig_w)
            target_h = int(orig_h * ratio)
            target_w = MIN_WIDTH
            image = cv2.resize(
                image, (target_w, target_h), interpolation=cv2.INTER_CUBIC
            )
        # If it's already wider than MIN_WIDTH, we do nothing.

    # 6. Save the final image
    # 6. Save the final image or return it
    if dst_path:
        success = cv2.imwrite(str(dst_path), image)
        if not success:
            raise IOError(f"Failed to write preprocessed image to {dst_path}")
        return None
    else:
        return image
