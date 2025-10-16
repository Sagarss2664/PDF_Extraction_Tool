# app/pdf_processor.py
import logging
import os
from typing import List, Dict, Any
import pdfplumber
import PyPDF2
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    PDF text extraction processor with fallback mechanisms
    """
    
    def __init__(self):
        self.supported_methods = ['pdfplumber', 'pypdf2']
        logger.info("PDF Processor initialized")
    
    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF using multiple methods with fallback
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        extracted_texts = []
        
        # Try pdfplumber first (better for text-based PDFs)
        text_pdfplumber = self._extract_with_pdfplumber(file_path)
        if text_pdfplumber and self._is_meaningful_text(text_pdfplumber):
            extracted_texts.append({
                "method": "pdfplumber",
                "text": text_pdfplumber,
                "pages": len(text_pdfplumber.split('\f')) if '\f' in text_pdfplumber else 1
            })
            logger.info(f"✅ Successfully extracted text using pdfplumber from {file_path}")
        
        # If pdfplumber fails or produces little text, try PyPDF2
        if not extracted_texts or len(text_pdfplumber.strip()) < 100:
            text_pypdf2 = self._extract_with_pypdf2(file_path)
            if text_pypdf2 and self._is_meaningful_text(text_pypdf2):
                extracted_texts.append({
                    "method": "pypdf2",
                    "text": text_pypdf2,
                    "pages": len(text_pypdf2.split('\f')) if '\f' in text_pypdf2 else 1
                })
                logger.info(f"✅ Successfully extracted text using PyPDF2 from {file_path}")
        
        if not extracted_texts:
            logger.warning(f"❌ No text could be extracted from {file_path}")
            raise ValueError(f"No extractable text found in PDF: {file_path}")
        
        # Combine all extracted texts
        combined_text = "\n\n".join([item["text"] for item in extracted_texts])
        
        # Split into manageable chunks if too large
        text_chunks = self._split_text(combined_text)
        
        result = []
        for i, chunk in enumerate(text_chunks):
            result.append({
                "chunk_id": i + 1,
                "text": chunk,
                "source_file": os.path.basename(file_path),
                "total_chunks": len(text_chunks)
            })
        
        logger.info(f"📊 Extracted {len(result)} text chunks from {file_path}")
        return result
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    def _is_meaningful_text(self, text: str) -> bool:
        """Check if extracted text is meaningful"""
        if not text or len(text.strip()) < 50:
            return False
        
        # Check if text contains meaningful words (not just random characters)
        words = text.split()
        if len(words) < 10:
            return False
        
        # Check for common financial terms as an indicator of meaningful content
        financial_indicators = ['fund', 'investment', 'capital', 'financial', 'company', 
                               'revenue', 'profit', 'loss', 'asset', 'liability']
        
        text_lower = text.lower()
        indicator_count = sum(1 for indicator in financial_indicators if indicator in text_lower)
        
        return indicator_count >= 2
    
    def _split_text(self, text: str, max_chunk_size: int = 10000) -> List[str]:
        """Split text into manageable chunks"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic information about PDF"""
        try:
            with pdfplumber.open(file_path) as pdf:
                return {
                    "page_count": len(pdf.pages),
                    "file_size": os.path.getsize(file_path),
                    "file_name": os.path.basename(file_path)
                }
        except Exception as e:
            logger.error(f"Failed to get PDF info: {str(e)}")
            return {}


# Utility function
def create_pdf_processor() -> PDFProcessor:
    return PDFProcessor()