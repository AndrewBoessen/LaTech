from pathlib import Path
from pylatex import Document, NoEscape

def compile_latex_to_pdf(latex_source_path: Path, pdf_out_path: Path) -> None:
    latex_content = latex_source_path.read_text(encoding="utf-8")
    
    # Create a new document
    doc = Document()
    
    # Add the LaTeX content
    doc.append(NoEscape(latex_content))
    
    # Compile the document
    doc.generate_pdf(str(pdf_out_path.with_suffix('')), clean_tex=False)