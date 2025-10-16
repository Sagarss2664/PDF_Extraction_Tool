from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List
from app.core.pdf_parser import extract_text_from_pdf
from app.core.llm_client import extract_structured_data

router = APIRouter()  # ✅ This line was missing

@router.post("/upload/")
async def upload_pdfs(
    pdfs: List[UploadFile] = File(...),
    template_id: str = Form(...)
):
    extracted_data = []

    for pdf in pdfs:
        content = await pdf.read()
        text = extract_text_from_pdf(content)
        structured = extract_structured_data(template_id, text)
        extracted_data.append({
            "filename": pdf.filename,
            "data": structured
        })

    return extracted_data