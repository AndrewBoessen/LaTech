from io import BytesIO
from pathlib import Path


MINIMAL_PDF = b"""%PDF-1.4\n1 0 obj<<>>endobj\n2 0 obj<</Length 44>>stream\nBT /F1 12 Tf 72 720 Td (Placeholder PDF) Tj ET\nendstream endobj\n3 0 obj<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>endobj\n4 0 obj<</Type /Page /Parent 5 0 R /Resources <</Font <</F1 3 0 R>>>> /MediaBox [0 0 612 792] /Contents 2 0 R>>endobj\n5 0 obj<</Type /Pages /Kids [4 0 R] /Count 1>>endobj\n6 0 obj<</Type /Catalog /Pages 5 0 R>>endobj\nxref\n0 7\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000170 00000 n \n0000000251 00000 n \n0000000401 00000 n \n0000000471 00000 n \ntrailer<</Size 7 /Root 6 0 R>>\nstartxref\n534\n%%EOF\n"""


def compile_latex_to_pdf(latex_source_path: Path, pdf_out_path: Path) -> None:
    # Placeholder: write a minimal PDF; ignore latex_source_path for now
    pdf_out_path.write_bytes(MINIMAL_PDF)


