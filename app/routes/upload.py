from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.ocr import extract_text
from app.services.parser import parse_mcq

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    pdf_text = extract_text(file_path)
    print("=== PDF TEXT START ===")
    print(pdf_text)
    print("=== PDF TEXT END ===")

    # Parse questions from extracted text
    questions = parse_mcq(pdf_text)

    # Return rendered template
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "filename": file.filename,
            "pdf_text": pdf_text,
            "questions": questions
        }
    )
