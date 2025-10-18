# from pathlib import Path
# from fastapi import FastAPI, File, UploadFile, HTTPException, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# import os
# from typing import List
# import uuid
# import logging
# from dotenv import load_dotenv
# from app.services.pdf_extractor import PDFExtractor
# from app.services.llm_processor import LLMProcessor
# from app.services.excel_generator import ExcelGenerator
# import sys

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# load_dotenv()

# app = FastAPI(title="PDF Extraction Tool", version="1.0.0")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Ensure upload and output directories exist
# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "output"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# @app.post("/api/extract")
# async def extract_data_from_pdfs(
#     files: List[UploadFile] = File(...),
#     template_id: int = Form(...)  # Changed from default value to Form parameter
# ):
#     """
#     Extract data from uploaded PDFs using the specified template
#     """
#     saved_files = []  # Initialize here to avoid UnboundLocalError
    
#     try:
#         # Validate template ID
#         if template_id not in [1, 2]:
#             raise HTTPException(status_code=400, detail="Invalid template ID. Use 1 or 2.")
        
#         # Validate files
#         if not files:
#             raise HTTPException(status_code=400, detail="No files uploaded")
        
#         logger.info(f"🔍 STARTING EXTRACTION - Template ID: {template_id}")
#         logger.info(f"📁 Files received: {[f.filename for f in files]}")
        
#         # Generate unique job ID
#         job_id = str(uuid.uuid4())
        
#         # Save uploaded files
#         saved_files = []
#         for file in files:
#             if not file.filename.lower().endswith('.pdf'):
#                 raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
#             file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
#             with open(file_path, "wb") as f:
#                 content = await file.read()
#                 f.write(content)
#             saved_files.append(file_path)
        
#         logger.info(f"💾 Saved {len(saved_files)} files for processing")
        
#         # Extract text from PDFs
#         pdf_extractor = PDFExtractor()
#         extracted_texts = []
#         for file_path in saved_files:
#             logger.info(f"📄 Processing PDF: {os.path.basename(file_path)}")
#             text = pdf_extractor.extract_text(file_path)
#             extracted_texts.append(text)
        
#         logger.info(f"📊 Total text segments extracted: {len(extracted_texts)}")
        
#         # Process with LLM
#         llm_processor = LLMProcessor()
#         logger.info(f"🧠 Processing with LLM using template: {template_id}")
#         structured_data = llm_processor.process_texts(extracted_texts, template_id)
        
#         logger.info(f"✅ LLM processing completed. Data keys: {list(structured_data.keys())}")
        
#         # Generate Excel file
#         excel_generator = ExcelGenerator()
#         output_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
#         excel_generator.generate_excel(structured_data, template_id, output_path)
        
#         # Clean up uploaded files
#         for file_path in saved_files:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
        
#         response_data = {
#             "job_id": job_id,
#             "status": "success",
#             "message": f"Data extracted successfully using Template {template_id}",
#             "template_used": template_id,
#             "download_url": f"/api/download/{job_id}"
#         }
        
#         logger.info(f"🎉 Extraction completed successfully for job {job_id}")
#         logger.info(f"📋 FINAL RESPONSE - Template used: {template_id}")
        
#         return response_data
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         # Clean up on error
#         for file_path in saved_files:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#         logger.error(f"❌ Extraction failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

# @app.get("/api/download/{job_id}")
# async def download_file(job_id: str):
#     """
#     Download the generated Excel file
#     """
#     file_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Generate filename based on template used (you might want to store this info)
#     filename = f"extracted_data_{job_id}.xlsx"
    
#     return FileResponse(
#         path=file_path,
#         filename=filename,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

# @app.get("/api/templates")
# async def get_available_templates():
#     """
#     Get list of available templates
#     """
#     return {
#         "templates": [
#             {"id": 1, "name": "Private Equity Fund Detailed Template", "description": "Comprehensive fund and investment data extraction"},
#             {"id": 2, "name": "Portfolio Summary Template", "description": "Executive portfolio and investment summary"}
#         ]
#     }

# @app.get("/api/health")
# async def health_check():
#     return {"status": "healthy", "service": "PDF Extraction Tool"}

# @app.get("/api/debug-env")
# async def debug_env():
#     """Debug endpoint to check environment variables"""
#     api_key = os.getenv("GROQ_API_KEY")  # Changed from OPENAI_API_KEY to GROQ_API_KEY
#     return {
#         "api_key_exists": bool(api_key),
#         "api_key_prefix": api_key[:10] + "..." if api_key else None,
#         "api_key_length": len(api_key) if api_key else 0,
#         "current_directory": os.getcwd(),
#         "python_path": sys.path,
#         "env_files_checked": [
#             str(Path(__file__).parent / '.env'),
#             str(Path(__file__).parent.parent / '.env'),
#             str(Path(__file__).parent.parent.parent / '.env')
#         ]
#     }

# @app.get("/")
# async def root():
#     return {"message": "PDF Extraction API is running"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
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
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="PDF Extraction Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload and output directories exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
CHUNK_SIZE = 1024 * 1024  # 1MB chunks
PROCESSING_TIMEOUT = 600  # 10 minutes

async def _extract_data_internal(files: List[UploadFile], template_id: int):
    """
    Internal function to handle PDF extraction with comprehensive logging
    """
    saved_files = []
    
    try:
        logger.info("🔍 [DEBUG] STARTING _extract_data_internal")
        logger.info(f"🔍 [DEBUG] Template ID: {template_id}")
        logger.info(f"🔍 [DEBUG] Number of files: {len(files)}")
        
        # Validate template ID
        if template_id not in [1, 2]:
            raise HTTPException(status_code=400, detail="Invalid template ID. Use 1 or 2.")
        
        # Validate files
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        logger.info("🔍 [DEBUG] Template and file validation passed")
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        logger.info(f"🔍 [DEBUG] Generated Job ID: {job_id}")
        
        # Save uploaded files with chunked reading
        logger.info("🔍 [DEBUG] Starting file upload process...")
        for file in files:
            logger.info(f"🔍 [DEBUG] Processing file: {file.filename}")
            
            # Check file extension
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # Check file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            logger.info(f"🔍 [DEBUG] File {file.filename} size: {file_size} bytes")
            
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds maximum size of 50MB")
            
            if file_size == 0:
                raise HTTPException(status_code=400, detail=f"File {file.filename} is empty")
            
            # Save file with chunked reading
            file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
            logger.info(f"🔍 [DEBUG] Saving file to: {file_path}")
            
            with open(file_path, "wb") as f:
                chunk_count = 0
                while True:
                    chunk = await file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
                    chunk_count += 1
                
                logger.info(f"🔍 [DEBUG] File saved in {chunk_count} chunks")
            
            saved_files.append(file_path)
            logger.info(f"🔍 [DEBUG] Successfully saved: {file.filename}")
        
        logger.info(f"💾 [DEBUG] Saved {len(saved_files)} files for processing")
        
        # Extract text from PDFs with comprehensive error handling
        pdf_extractor = PDFExtractor()
        extracted_texts = []
        
        logger.info("🔍 [DEBUG] Starting PDF text extraction...")
        for i, file_path in enumerate(saved_files):
            logger.info(f"🔍 [DEBUG] Processing PDF {i+1}/{len(saved_files)}: {os.path.basename(file_path)}")
            
            try:
                # FIX: PDFExtractor returns a dictionary, not a string
                extraction_result = pdf_extractor.extract_text(file_path)
                logger.info(f"🔍 [DEBUG] PDF extraction completed for {os.path.basename(file_path)}")
                
                # Check if extraction was successful
                if extraction_result.get("status") != "success":
                    logger.error(f"❌ [DEBUG] PDF extraction failed: {extraction_result.get('error', 'Unknown error')}")
                    extracted_texts.append("PDF_EXTRACTION_FAILED")
                    continue
                
                # Extract the actual text content from the result dictionary
                text = extraction_result.get("text", "")
                char_count = extraction_result.get("char_count", 0)
                page_count = extraction_result.get("page_count", 0)
                
                logger.info(f"🔍 [DEBUG] Extraction details - Pages: {page_count}, Chars: {char_count}, Status: {extraction_result.get('status')}")
                logger.info(f"🔍 [DEBUG] Financial score: {extraction_result.get('financial_content_score', 0)}")
                logger.info(f"🔍 [DEBUG] Tables found: {len(extraction_result.get('tables', []))}")
                
                # Safe text preview logging
                if text and isinstance(text, str):
                    preview = text[:200] + "..." if len(text) > 200 else text
                    logger.info(f"🔍 [DEBUG] First 200 chars: {preview}")
                else:
                    logger.warning(f"🔍 [DEBUG] Text is empty or not string. Type: {type(text)}")
                
                # Validate extracted text
                if not text or len(text.strip()) < 10:
                    logger.warning(f"⚠️ [DEBUG] Little or no text extracted from {os.path.basename(file_path)}")
                    text = "PDF_CONTENT_UNAVAILABLE"
                elif len(text.strip()) < 50:
                    logger.warning(f"⚠️ [DEBUG] Minimal text extracted from {os.path.basename(file_path)}: {len(text)} chars")
                
                extracted_texts.append(text)
                logger.info(f"🔍 [DEBUG] Successfully processed PDF {i+1}")
                
            except Exception as e:
                logger.error(f"❌ [DEBUG] Failed to extract text from {file_path}: {str(e)}")
                logger.error(f"❌ [DEBUG] Error type: {type(e).__name__}")
                extracted_texts.append("PDF_EXTRACTION_FAILED")
        
        logger.info(f"📊 [DEBUG] Total text segments extracted: {len(extracted_texts)}")
        logger.info(f"📊 [DEBUG] Extraction status: {[ 'SUCCESS' if text not in ['PDF_CONTENT_UNAVAILABLE', 'PDF_EXTRACTION_FAILED'] else 'FAILED' for text in extracted_texts ]}")
        
        # Validate texts before LLM processing
        valid_texts = []
        for i, text in enumerate(extracted_texts):
            if text in ["PDF_CONTENT_UNAVAILABLE", "PDF_EXTRACTION_FAILED"]:
                logger.warning(f"⚠️ [DEBUG] Skipping file {i} due to extraction failure")
                continue
            if len(text.strip()) < 50:
                logger.warning(f"⚠️ [DEBUG] File {i} has insufficient text: {len(text)} chars")
                continue
            valid_texts.append(text)
        
        logger.info(f"🔍 [DEBUG] Valid texts for LLM processing: {len(valid_texts)}/{len(extracted_texts)}")
        
        if not valid_texts:
            raise HTTPException(status_code=400, detail="No valid PDF content could be extracted from any file")
        
        # Process with LLM
        llm_processor = LLMProcessor()
        logger.info(f"🧠 [DEBUG] Starting LLM processing with template: {template_id}")
        logger.info(f"🧠 [DEBUG] Number of valid texts to process: {len(valid_texts)}")
        
        try:
            structured_data = llm_processor.process_texts(valid_texts, template_id)
            logger.info(f"✅ [DEBUG] LLM processing completed successfully")
            logger.info(f"✅ [DEBUG] Data keys returned: {list(structured_data.keys()) if structured_data else 'None'}")
            
            if not structured_data:
                logger.warning("⚠️ [DEBUG] LLM returned empty structured data")
                structured_data = {"error": "No data could be extracted"}
                
        except Exception as e:
            logger.error(f"❌ [DEBUG] LLM processing failed: {str(e)}")
            logger.error(f"❌ [DEBUG] LLM error type: {type(e).__name__}")
            raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")
        
        # Generate Excel file
        excel_generator = ExcelGenerator()
        output_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
        logger.info(f"📊 [DEBUG] Generating Excel file at: {output_path}")
        
        try:
            excel_generator.generate_excel(structured_data, template_id, output_path)
            logger.info(f"✅ [DEBUG] Excel file generated successfully")
            
            # Verify file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ [DEBUG] Output file created: {output_path} ({file_size} bytes)")
            else:
                logger.error(f"❌ [DEBUG] Output file was not created: {output_path}")
                raise HTTPException(status_code=500, detail="Failed to create output file")
                
        except Exception as e:
            logger.error(f"❌ [DEBUG] Excel generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Excel generation failed: {str(e)}")
        
        # Clean up uploaded files
        logger.info("🔍 [DEBUG] Cleaning up uploaded files...")
        cleanup_count = 0
        for file_path in saved_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    cleanup_count += 1
                    logger.info(f"🔍 [DEBUG] Cleaned up: {os.path.basename(file_path)}")
                except Exception as cleanup_error:
                    logger.error(f"⚠️ [DEBUG] Cleanup failed for {file_path}: {cleanup_error}")
        
        logger.info(f"🔍 [DEBUG] Cleaned up {cleanup_count}/{len(saved_files)} files")
        
        # Prepare response
        response_data = {
            "job_id": job_id,
            "status": "success",
            "message": f"Data extracted successfully using Template {template_id}",
            "template_used": template_id,
            "download_url": f"/api/download/{job_id}",
            "files_processed": len(files),
            "files_successful": len(valid_texts),
            "files_failed": len(files) - len(valid_texts)
        }
        
        logger.info(f"🎉 [DEBUG] Extraction completed successfully for job {job_id}")
        logger.info(f"📋 [DEBUG] FINAL RESPONSE - Template used: {template_id}")
        logger.info(f"📋 [DEBUG] Response data: {response_data}")
        
        return response_data
        
    except HTTPException:
        logger.error("🔍 [DEBUG] HTTPException raised in _extract_data_internal")
        raise
    except Exception as e:
        logger.error(f"❌ [DEBUG] Unhandled exception in _extract_data_internal: {str(e)}")
        logger.error(f"❌ [DEBUG] Exception type: {type(e).__name__}")
        
        # Enhanced cleanup on error
        if 'saved_files' in locals():
            logger.info("🔍 [DEBUG] Starting emergency cleanup...")
            cleanup_count = 0
            for file_path in saved_files:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        cleanup_count += 1
                        logger.info(f"🔍 [DEBUG] Emergency cleanup: {os.path.basename(file_path)}")
                    except Exception as cleanup_error:
                        logger.error(f"⚠️ [DEBUG] Emergency cleanup failed for {file_path}: {cleanup_error}")
            logger.info(f"🔍 [DEBUG] Emergency cleanup completed: {cleanup_count} files")
        
        # Provide more specific error messages
        error_msg = str(e).lower()
        if "pdf" in error_msg or "extract" in error_msg:
            raise HTTPException(status_code=400, detail=f"PDF processing error: {str(e)}")
        elif "memory" in error_msg:
            raise HTTPException(status_code=413, detail="File too large to process")
        elif "timeout" in error_msg:
            raise HTTPException(status_code=408, detail="Processing timeout")
        else:
            raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.post("/api/extract")
async def extract_data_from_pdfs(
    files: List[UploadFile] = File(...),
    template_id: int = Form(...)
):
    """
    Extract data from uploaded PDFs using the specified template
    """
    logger.info("🚀 [DEBUG] ========== NEW EXTRACTION REQUEST ==========")
    logger.info(f"🚀 [DEBUG] Endpoint: /api/extract")
    logger.info(f"🚀 [DEBUG] Template ID: {template_id}")
    logger.info(f"🚀 [DEBUG] Files received: {[f.filename for f in files]}")
    
    try:
        # Set timeout for entire operation
        logger.info(f"⏰ [DEBUG] Setting processing timeout: {PROCESSING_TIMEOUT} seconds")
        result = await asyncio.wait_for(
            _extract_data_internal(files, template_id), 
            timeout=PROCESSING_TIMEOUT
        )
        logger.info("✅ [DEBUG] Extraction completed within timeout")
        return result
        
    except asyncio.TimeoutError:
        logger.error("⏰ [DEBUG] Extraction timed out!")
        raise HTTPException(status_code=408, detail="Extraction timed out. Please try with smaller files or fewer PDFs.")
    except HTTPException:
        logger.error("🔍 [DEBUG] HTTPException propagated to main endpoint")
        raise
    except Exception as e:
        logger.error(f"❌ [DEBUG] Unexpected error in main endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/api/download/{job_id}")
async def download_file(job_id: str):
    """
    Download the generated Excel file
    """
    logger.info(f"📥 [DEBUG] Download request for job_id: {job_id}")
    
    file_path = os.path.join(OUTPUT_DIR, f"{job_id}_extracted_data.xlsx")
    logger.info(f"📥 [DEBUG] Looking for file at: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"❌ [DEBUG] File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found or has expired")
    
    # Get file info
    file_size = os.path.getsize(file_path)
    logger.info(f"📥 [DEBUG] File found: {file_path} ({file_size} bytes)")
    
    filename = f"extracted_data_{job_id}.xlsx"
    logger.info(f"📥 [DEBUG] Serving file as: {filename}")
    
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
    logger.info("🔍 [DEBUG] Templates list requested")
    return {
        "templates": [
            {"id": 1, "name": "Private Equity Fund Detailed Template", "description": "Comprehensive fund and investment data extraction"},
            {"id": 2, "name": "Portfolio Summary Template", "description": "Executive portfolio and investment summary"}
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    logger.info("🔍 [DEBUG] Health check requested")
    
    # Check if directories exist
    upload_dir_exists = os.path.exists(UPLOAD_DIR)
    output_dir_exists = os.path.exists(OUTPUT_DIR)
    
    health_status = {
        "status": "healthy", 
        "service": "PDF Extraction Tool",
        "upload_dir": upload_dir_exists,
        "output_dir": output_dir_exists,
        "timestamp": str(asyncio.get_event_loop().time())
    }
    
    logger.info(f"🔍 [DEBUG] Health status: {health_status}")
    return health_status

@app.get("/api/debug-env")
async def debug_env():
    """Debug endpoint to check environment variables"""
    logger.info("🔍 [DEBUG] Environment debug requested")
    
    api_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    debug_info = {
        "groq_api_key_exists": bool(api_key),
        "groq_api_key_prefix": api_key[:10] + "..." if api_key else None,
        "groq_api_key_length": len(api_key) if api_key else 0,
        "openai_api_key_exists": bool(openai_key),
        "openai_api_key_prefix": openai_key[:10] + "..." if openai_key else None,
        "current_directory": os.getcwd(),
        "upload_dir": UPLOAD_DIR,
        "output_dir": OUTPUT_DIR,
        "upload_dir_contents": os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else "NOT_FOUND",
        "output_dir_contents": os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else "NOT_FOUND",
        "python_version": sys.version,
        "env_files_checked": [
            str(Path(__file__).parent / '.env'),
            str(Path(__file__).parent.parent / '.env'),
            str(Path(__file__).parent.parent.parent / '.env')
        ]
    }
    
    logger.info(f"🔍 [DEBUG] Environment debug info: {debug_info}")
    return debug_info

@app.get("/api/debug-files")
async def debug_files():
    """Debug endpoint to check file system status"""
    logger.info("🔍 [DEBUG] Filesystem debug requested")
    
    debug_info = {
        "upload_dir": {
            "exists": os.path.exists(UPLOAD_DIR),
            "file_count": len(os.listdir(UPLOAD_DIR)) if os.path.exists(UPLOAD_DIR) else 0,
            "files": os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else []
        },
        "output_dir": {
            "exists": os.path.exists(OUTPUT_DIR),
            "file_count": len(os.listdir(OUTPUT_DIR)) if os.path.exists(OUTPUT_DIR) else 0,
            "files": os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []
        },
        "current_working_dir": os.getcwd(),
        "disk_usage": {
            "free_gb": round(os.path.getfree(".") / (1024**3), 2) if hasattr(os, 'getfree') else "N/A",
            "total_gb": round(os.path.gettotal(".") / (1024**3), 2) if hasattr(os, 'gettotal') else "N/A"
        }
    }
    
    logger.info(f"🔍 [DEBUG] Filesystem debug info: {debug_info}")
    return debug_info

@app.get("/")
async def root():
    logger.info("🔍 [DEBUG] Root endpoint accessed")
    return {"message": "PDF Extraction API is running", "version": "1.0.0"}

if __name__ == "__main__":
    logger.info("🔍 [DEBUG] Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")