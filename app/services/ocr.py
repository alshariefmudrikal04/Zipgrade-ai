from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

def extract_text(pdf_path: Path) -> str:
    text = ""
    pages = convert_from_path(str(pdf_path))
    for page in pages:
        text += pytesseract.image_to_string(page)
        text += "\n"
    return text
