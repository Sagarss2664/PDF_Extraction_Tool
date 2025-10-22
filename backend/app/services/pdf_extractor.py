# pdf_extractor.py
import pdfplumber
import logging
from typing import Dict, Any, List, Tuple
import os
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self):
        self.financial_keywords = [
            'financial', 'statement', 'balance', 'income', 'cash flow', 'revenue',
            'ebitda', 'nav', 'irr', 'multiple', 'commitment', 'investment',
            'portfolio', 'valuation', 'performance', 'fund', 'capital', 'management',
            'fee', 'distribution', 'contribution', 'proceeds', 'realized', 'unrealized'
        ]
    
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF file with financial document optimization
        """
        logger.info(f"📄 Starting PDF extraction from: {file_path}")
        
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                error_msg = f"PDF file not found: {file_path}"
                logger.error(error_msg)
                return self._create_error_response(file_path, error_msg)
            
            text_content = ""
            metadata = {}
            page_count = 0
            char_count = 0
            financial_content_score = 0
            
            with pdfplumber.open(file_path) as pdf:
                # Extract metadata
                metadata = pdf.metadata or {}
                page_count = len(pdf.pages)
                
                logger.info(f"📖 Processing {page_count} pages from {file_path}")
                
                # Extract text from each page with financial content detection
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = self._extract_page_text(page, page_num + 1)
                        if page_text:
                            text_content += page_text
                            char_count += len(page_text)
                            
                            # Score page for financial content
                            page_score = self._score_financial_content(page_text)
                            financial_content_score += page_score
                            
                            logger.debug(f"✅ Extracted {len(page_text)} chars from page {page_num + 1} (score: {page_score})")
                        else:
                            logger.warning(f"⚠️ No text extracted from page {page_num + 1}")
                    except Exception as page_error:
                        logger.warning(f"⚠️ Error extracting text from page {page_num + 1}: {page_error}")
                        continue
            
            # Extract tables separately for financial data
            tables_data = self._extract_tables(file_path)
            
            result = {
                "file_path": file_path,
                "metadata": metadata,
                "text": text_content.strip(),
                "page_count": page_count,
                "char_count": char_count,
                "financial_content_score": financial_content_score,
                "tables": tables_data,
                "status": "success",
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Successfully extracted {char_count} characters from {page_count} pages")
            logger.info(f"💰 Financial content score: {financial_content_score}")
            logger.info(f"📊 Tables extracted: {len(tables_data)}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to extract text from PDF: {str(e)}"
            logger.error(f"❌ {error_msg}")
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
            
            return self._create_error_response(file_path, error_msg)
    
    def _extract_page_text(self, page, page_num: int) -> str:
        """Extract and clean text from a single page"""
        try:
            text = page.extract_text()
            if not text or not text.strip():
                return ""
            
            # Clean and structure the text
            cleaned_text = self._clean_text(text, page_num)
            return cleaned_text
            
        except Exception as e:
            logger.warning(f"Error processing page {page_num}: {e}")
            return ""

    def _clean_text(self, text: str, page_num: int) -> str:
        """Clean and structure extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR issues in financial documents
        text = self._fix_common_ocr_errors(text)
        
        # Structure with page header
        structured_text = f"===== Page {page_num} =====\n\n{text.strip()}\n\n"
        
        return structured_text

    def _fix_common_ocr_errors(self, text: str) -> str:
        """Fix common OCR errors in financial documents"""
        replacements = {
            r'\b([A-Z])\s+([A-Z])\b': r'\1\2',  # Fix spaced acronyms
            r'(\d)\s+(\d)': r'\1\2',  # Fix spaced numbers
            r'\$(\s+)(\d)': r'$\2',  # Fix dollar sign spacing
            r'(\d)\s*%\s*': r'\1% ',  # Fix percentage spacing
            r'\bI\s*R\s*R\b': 'IRR',  # Fix IRR acronym
            r'\bN\s*A\s*V\b': 'NAV',  # Fix NAV acronym
            r'\bE\s*B\s*I\s*T\s*D\s*A\b': 'EBITDA',  # Fix EBITDA acronym
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        return text

    def _score_financial_content(self, text: str) -> int:
        """Score text for financial content relevance"""
        if not text:
            return 0
        
        text_lower = text.lower()
        score = 0
        
        # Check for financial keywords
        for keyword in self.financial_keywords:
            if keyword in text_lower:
                score += 2
        
        # Check for financial patterns
        financial_patterns = [
            r'\$\d+[,.]?\d*',  # Currency amounts
            r'\d+[,.]?\d*\s*%',  # Percentages
            r'\b\d{4}-\d{2}-\d{2}\b',  # Dates
            r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',  # Month-year
        ]
        
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_lower)
            score += len(matches)
        
        # Bonus for tables and structured data
        if re.search(r'\b(table|schedule|statement|summary)\b', text_lower, re.IGNORECASE):
            score += 5
        
        return min(score, 20)  # Cap the score

    def _extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract tables from PDF with financial data optimization"""
        tables_data = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        tables = page.extract_tables()
                        if tables:
                            for table_num, table in enumerate(tables):
                                if self._is_financial_table(table):
                                    table_data = {
                                        "page": page_num + 1,
                                        "table_number": table_num + 1,
                                        "data": table,
                                        "rows": len(table),
                                        "financial_score": self._score_table_financial_content(table)
                                    }
                                    tables_data.append(table_data)
                                    logger.debug(f"📊 Found financial table {table_num + 1} on page {page_num + 1}")
                    except Exception as table_error:
                        logger.warning(f"Error extracting tables from page {page_num + 1}: {table_error}")
                        continue
            
        except Exception as e:
            logger.warning(f"Error during table extraction: {e}")
        
        return tables_data

    def _is_financial_table(self, table: List[List[str]]) -> bool:
        """Check if table contains financial data"""
        if not table or len(table) < 2:
            return False
        
        # Check header row for financial indicators
        header_row = ' '.join(str(cell) for cell in table[0] if cell)
        header_lower = header_row.lower()
        
        financial_indicators = [
            'amount', 'value', 'price', 'cost', 'total', 'sum', 'balance',
            'revenue', 'income', 'expense', 'profit', 'loss', 'cash', 'fund',
            'investment', 'capital', 'fee', 'rate', 'percentage', 'irr', 'nav'
        ]
        
        return any(indicator in header_lower for indicator in financial_indicators)

    def _score_table_financial_content(self, table: List[List[str]]) -> int:
        """Score table for financial content"""
        if not table:
            return 0
        
        score = 0
        all_text = ' '.join(' '.join(str(cell) for cell in row if cell) for row in table)
        text_lower = all_text.lower()
        
        # Check for financial keywords
        for keyword in self.financial_keywords:
            if keyword in text_lower:
                score += 3
        
        # Check for currency symbols and numbers
        currency_matches = re.findall(r'[\$\£\€]\s*\d+[,.]?\d*', all_text)
        score += len(currency_matches) * 2
        
        # Check for percentage values
        percentage_matches = re.findall(r'\d+[,.]?\d*\s*%', all_text)
        score += len(percentage_matches)
        
        return min(score, 25)

    def extract_with_layout(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text with layout information for tables (enhanced version)
        """
        logger.info(f"🔍 Starting enhanced layout extraction from: {file_path}")
        
        try:
            if not os.path.exists(file_path):
                error_msg = f"PDF file not found: {file_path}"
                logger.error(error_msg)
                return self._create_error_response(file_path, error_msg)
            
            result = {
                "file_path": file_path,
                "pages": [],
                "tables": [],
                "financial_tables": [],
                "status": "success",
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            table_count = 0
            financial_table_count = 0
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_data = {
                        "page_number": page_num + 1,
                        "text": page.extract_text() or "",
                        "tables": [],
                        "financial_tables": []
                    }
                    
                    # Extract tables with enhanced detection
                    try:
                        tables = page.extract_tables()
                        for table_num, table in enumerate(tables):
                            if table and any(any(cell for cell in row) for row in table):
                                table_data = {
                                    "table_number": table_num + 1,
                                    "data": table,
                                    "rows": len(table),
                                    "columns": len(table[0]) if table else 0
                                }
                                
                                page_data["tables"].append(table_data)
                                result["tables"].append({
                                    "page": page_num + 1,
                                    "table_number": table_num + 1,
                                    "data": table
                                })
                                table_count += 1
                                
                                # Check if it's a financial table
                                if self._is_financial_table(table):
                                    financial_score = self._score_table_financial_content(table)
                                    financial_table_data = {
                                        **table_data,
                                        "financial_score": financial_score
                                    }
                                    page_data["financial_tables"].append(financial_table_data)
                                    result["financial_tables"].append(financial_table_data)
                                    financial_table_count += 1
                                    logger.debug(f"💰 Found financial table {table_num + 1} on page {page_num + 1} (score: {financial_score})")
                                
                                logger.debug(f"📊 Found table {table_num + 1} on page {page_num + 1}")
                    except Exception as table_error:
                        logger.warning(f"⚠️ Error extracting tables from page {page_num + 1}: {table_error}")
                    
                    result["pages"].append(page_data)
            
            result["table_count"] = table_count
            result["financial_table_count"] = financial_table_count
            result["page_count"] = len(result["pages"])
            
            logger.info(f"✅ Enhanced layout extraction completed: {table_count} total tables, {financial_table_count} financial tables across {len(result['pages'])} pages")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to extract PDF layout: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return self._create_error_response(file_path, error_msg)

    def _create_error_response(self, file_path: str, error_msg: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "file_path": file_path,
            "error": error_msg,
            "status": "error",
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "tables": [],
            "extraction_timestamp": datetime.now().isoformat()
        }

    def extract_financial_sections(self, file_path: str) -> Dict[str, Any]:
        """
        Extract and identify financial sections from PDF
        """
        logger.info(f"💰 Extracting financial sections from: {file_path}")
        
        try:
            text_result = self.extract_text(file_path)
            if text_result.get("status") != "success":
                return text_result
            
            text_content = text_result["text"]
            financial_sections = self._identify_financial_sections(text_content)
            
            result = {
                **text_result,
                "financial_sections": financial_sections,
                "section_count": len(financial_sections)
            }
            
            logger.info(f"✅ Identified {len(financial_sections)} financial sections")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to extract financial sections: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return self._create_error_response(file_path, error_msg)

    def _identify_financial_sections(self, text: str) -> List[Dict[str, Any]]:
        """Identify and extract financial sections from text"""
        sections = []
        
        if not text:
            return sections
        
        # Common financial section headers
        section_patterns = [
            (r'(?:financial\s+)?statement\s+of\s+(?:operations|income)', 'Statement of Operations'),
            (r'balance\s+sheet', 'Balance Sheet'),
            (r'cash\s+flow\s+statement', 'Cash Flow Statement'),
            (r'schedule\s+of\s+investments', 'Schedule of Investments'),
            (r'portfolio\s+summary', 'Portfolio Summary'),
            (r'executive\s+summary', 'Executive Summary'),
            (r'performance\s+metrics', 'Performance Metrics'),
            (r'fund\s+summary', 'Fund Summary'),
            (r'investment\s+summary', 'Investment Summary'),
            (r'valuation\s+summary', 'Valuation Summary'),
        ]
        
        lines = text.split('\n')
        current_section = None
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean:
                continue
            
            # Check if line matches a section header
            for pattern, section_name in section_patterns:
                if re.search(pattern, line_clean, re.IGNORECASE):
                    if current_section:
                        sections.append(current_section)
                    
                    current_section = {
                        "name": section_name,
                        "content": line_clean + "\n",
                        "start_line": i,
                        "score": self._score_financial_content(line_clean)
                    }
                    break
            else:
                # Continue current section
                if current_section:
                    current_section["content"] += line_clean + "\n"
        
        # Add the last section
        if current_section:
            sections.append(current_section)
        
        return sections
    # End of pdf_extractor.py