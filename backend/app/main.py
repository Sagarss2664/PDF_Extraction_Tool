from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from typing import List
import uuid
import logging
from dotenv import load_dotenv
from app.services.pdf_extractor import PDFExtractor
from app.services.llm_processor import LLMProcessor
from app.services.excel_generator import ExcelGenerator
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="PDF Extraction Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload and output directories exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/api/extract")
async def extract_data_from_pdfs(
    files: List[UploadFile] = File(...),
    template_id: int = Form(...)  # Changed from default value to Form parameter
):
    """
    Extract data from uploaded PDFs using the specified template
    """
    saved_files = []  # Initialize here to avoid UnboundLocalError
    
    try:
        # Validate template ID
        if template_id not in [1, 2]:
            raise HTTPException(status_code=400, detail="Invalid template ID. Use 1 or 2.")
        
        # Validate files
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        logger.info(f"🔍 STARTING EXTRACTION - Template ID: {template_id}")
        logger.info(f"📁 Files received: {[f.filename for f in files]}")
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded files
        saved_files = []
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            saved_files.append(file_path)
        
        logger.info(f"💾 Saved {len(saved_files)} files for processing")
        
        # Extract text from PDFs
        pdf_extractor = PDFExtractor()
        extracted_texts = []
        for file_path in saved_files:
            logger.info(f"📄 Processing PDF: {os.path.basename(file_path)}")
            text = pdf_extractor.extract_text(file_path)
            extracted_texts.append(text)
        
        logger.info(f"📊 Total text segments extracted: {len(extracted_texts)}")
        
        # Process with LLM
        llm_processor = LLMProcessor()
        logger.info(f"🧠 Processing with LLM using template: {template_id}")
        structured_data = llm_processor.process_texts(extracted_texts, template_id)
        
        logger.info(f"✅ LLM processing completed. Data keys: {list(structured_data.keys())}")
        
        # Generate Excel file
        excel_generator = ExcelGenerator()
        output_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
        excel_generator.generate_excel(structured_data, template_id, output_path)
        
        # Clean up uploaded files
        for file_path in saved_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        response_data = {
            "job_id": job_id,
            "status": "success",
            "message": f"Data extracted successfully using Template {template_id}",
            "template_used": template_id,
            "download_url": f"/api/download/{job_id}"
        }
        
        logger.info(f"🎉 Extraction completed successfully for job {job_id}")
        logger.info(f"📋 FINAL RESPONSE - Template used: {template_id}")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        for file_path in saved_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        logger.error(f"❌ Extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.get("/api/download/{job_id}")
async def download_file(job_id: str):
    """
    Download the generated Excel file
    """
    file_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Generate filename based on template used (you might want to store this info)
    filename = f"extracted_data_{job_id}.xlsx"
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/api/templates")
async def get_available_templates():
    """
    Get list of available templates
    """
    return {
        "templates": [
            {"id": 1, "name": "Private Equity Fund Detailed Template", "description": "Comprehensive fund and investment data extraction"},
            {"id": 2, "name": "Portfolio Summary Template", "description": "Executive portfolio and investment summary"}
        ]
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "PDF Extraction Tool"}

@app.get("/api/debug-env")
async def debug_env():
    """Debug endpoint to check environment variables"""
    api_key = os.getenv("GROQ_API_KEY")  # Changed from OPENAI_API_KEY to GROQ_API_KEY
    return {
        "api_key_exists": bool(api_key),
        "api_key_prefix": api_key[:10] + "..." if api_key else None,
        "api_key_length": len(api_key) if api_key else 0,
        "current_directory": os.getcwd(),
        "python_path": sys.path,
        "env_files_checked": [
            str(Path(__file__).parent / '.env'),
            str(Path(__file__).parent.parent / '.env'),
            str(Path(__file__).parent.parent.parent / '.env')
        ]
    }

@app.get("/")
async def root():
    return {"message": "PDF Extraction API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)