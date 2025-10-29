from pathlib import Path
from typing import Optional

from ..models.schemas import PreprocessOptions


def apply_preprocessing(src_path: Path, dst_path: Path, options: PreprocessOptions) -> None:
    # Placeholder: copy file without modification for now
    dst_path.write_bytes(src_path.read_bytes())


