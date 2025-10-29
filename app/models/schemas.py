from typing import Optional
from pydantic import BaseModel


class PreprocessResize(BaseModel):
    width: int
    height: int


class PreprocessOptions(BaseModel):
    grayscale: bool = True
    denoise: bool = False
    threshold: Optional[int] = None
    resize: Optional[PreprocessResize] = None


class UploadResponse(BaseModel):
    uploadId: str


class PreprocessResponse(BaseModel):
    processedId: str


class ConvertResponse(BaseModel):
    latexId: str
    latex: str


class CompileRequest(BaseModel):
    latex: Optional[str] = None
    latexId: Optional[str] = None


class CompileResponse(BaseModel):
    pdfId: str


class StatusResponse(BaseModel):
    state: str
    progress: int
    error: Optional[str] = None


