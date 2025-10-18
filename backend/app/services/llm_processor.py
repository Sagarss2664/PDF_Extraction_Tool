# import json
# import logging
# import os
# import re
# import time
# from typing import List, Dict, Any, Optional
# from pathlib import Path
# from datetime import datetime
# import hashlib
# from groq import Groq
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)

# class LLMProcessor:
#     """
#     Enhanced LLM Processor with detailed template-specific prompts
#     """
    
#     def __init__(self, cache_enabled: bool = True):
#         self.cache_enabled = cache_enabled
#         self.response_cache = {}
#         self.usage_stats = {
#             "total_requests": 0,
#             "successful_extractions": 0,
#             "failed_extractions": 0,
#             "cache_hits": 0
#         }
        
#         self._setup_environment()
#         self._initialize_clients()
#         self.template_configs = self._initialize_template_configs()
        
#         logger.info("LLM Processor initialized successfully")

#     def _setup_environment(self):
#         """Setup environment variables"""
#         try:
#             possible_env_paths = [
#                 Path(__file__).parent.parent.parent / '.env',
#                 Path(__file__).parent / '.env',
#                 Path.cwd() / '.env',
#             ]
            
#             env_loaded = False
#             for env_path in possible_env_paths:
#                 if env_path.exists():
#                     load_dotenv(env_path)
#                     logger.info(f"Loaded environment from: {env_path}")
#                     env_loaded = True
#                     break
            
#             if not env_loaded:
#                 logger.warning("No .env file found, relying on system environment variables")
            
#             self.api_key = os.getenv("GROQ_API_KEY")
#             if not self.api_key:
#                 raise ValueError("GROQ_API_KEY not found in environment variables")
                
#         except Exception as e:
#             logger.error(f"Environment setup failed: {str(e)}")
#             raise

#     def _initialize_clients(self):
#         """Initialize Groq client"""
#         try:
#             self.client = Groq(api_key=self.api_key)
            
#             # Simplified model list for better reliability
#             self.available_models = [
#                 {
#                     "name": "llama-3.3-70b-versatile",
#                     "priority": 1,
#                     "max_tokens": 8000  # Increased for larger responses
#                 },
#                 {
#                     "name": "llama-3.1-8b-instant", 
#                     "priority": 2,
#                     "max_tokens": 8000
#                 }
#             ]
            
#             logger.info(f"Initialized Groq client with {len(self.available_models)} models")
            
#         except Exception as e:
#             logger.error(f"Client initialization failed: {str(e)}")
#             raise

#     def _initialize_template_configs(self) -> Dict[int, Dict[str, Any]]:
#         """Initialize detailed template configurations"""
#         return {
#             1: self._get_template_1_config(),
#             2: self._get_template_2_config()
#         }

#     def _get_template_1_config(self) -> Dict[str, Any]:
#         """Configuration for Template 1 - Private Equity Fund"""
#         return {
#             "name": "Private Equity Fund Detailed Template",
#             "description": "Comprehensive private equity fund data extraction",
#             "version": "1.3.0",
#             "sheets": [
#                 "Fund and Investment Vehicle Information",
#                 "Fund Manager", 
#                 "Fund Investment Vehicle Financial Position",
#                 "LP Investor Cashflows",
#                 "Fund Companies",
#                 "Initial Investments",
#                 "Company Investment Positions", 
#                 "Company Valuation",
#                 "Company Financials",
#                 "Investment History",
#                 "Reference Values"
#             ],
#             "json_schema": self._get_template_1_json_schema(),
#             "extraction_guidelines": self._get_template_1_extraction_guidelines(),
#             "specific_fields": self._get_template_1_specific_fields()
#         }

#     def _get_template_2_config(self) -> Dict[str, Any]:
#         """Configuration for Template 2 - Portfolio Summary"""
#         return {
#             "name": "Portfolio Summary Template",
#             "description": "Executive portfolio summary and investment data",
#             "version": "1.2.0",
#             "sheets": [
#                 "Executive Portfolio Summary",
#                 "Schedule of Investments",
#                 "Statement of Operations", 
#                 "Statements of Cashflows",
#                 "PCAP Statements",
#                 "Portfolio Companies Profile",
#                 "Portfolio Companies Financials",
#                 "FootNotes",
#                 "Reference Values"
#             ],
#             "json_schema": self._get_template_2_json_schema(),
#             "extraction_guidelines": self._get_template_2_extraction_guidelines(),
#             "specific_fields": self._get_template_2_specific_fields()
#         }

#     def _get_template_1_json_schema(self) -> Dict[str, Any]:
#         """Enhanced JSON schema for Template 1"""
#         return {
#             "Fund_and_Investment_Vehicle_Information": {
#                 "Fund_Details": {
#                     "Fund_Name": "string or null",
#                     "Fund_Currency": "string or null",
#                     "Fund_Legal_Structure": "string or null",
#                     "Fund_Domicile": "string or null",
#                     "Fund_Size": "number or null",
#                     "Total_Commitments": "number or null",
#                     "Vintage_Year": "number or null",
#                     "Financial_Year_End": "string or null"
#                 },
#                 "Key_Dates": {
#                     "Inception_Date": "string or null",
#                     "Final_Closing_Date": "string or null",
#                     "Investment_Period_End_Date": "string or null"
#                 },
#                 "Fee_Structure": {
#                     "Management_Fee_Rate": "number or null",
#                     "Carried_Interest_Percentage": "number or null",
#                     "Hurdle_Rate": "number or null"
#                 },
#                 "Investment_Focus": {
#                     "Geography_Focus": "string or null",
#                     "Sector_Focus": "string or null",
#                     "Stage_Focus": "string or null"
#                 }
#             },
#             "Fund_Manager": {
#                 "Management_Company": {
#                     "Management_Company_Name": "string or null",
#                     "Manager_Website": "string or null",
#                     "Primary_Contact": "string or null",
#                     "Contact_Email": "string or null",
#                     "Contact_Phone": "string or null",
#                     "Office_Address": "string or null"
#                 },
#                 "Firm_Details": {
#                     "Assets_Under_Management": "number or null",
#                     "Number_of_Investment_Professionals": "number or null",
#                     "Year_Founded": "number or null"
#                 }
#             },
#             "Fund_Investment_Vehicle_Financial_Position": {
#                 "Commitment_Summary": {
#                     "Total_Commitment": "number or null",
#                     "Paid_In_Capital": "number or null",
#                     "Remaining_Commitment": "number or null"
#                 },
#                 "Capital_Account": {
#                     "Total_Contributions": "number or null",
#                     "Total_Distributions": "number or null",
#                     "Invested_Capital": "number or null",
#                     "Realized_Proceeds": "number or null",
#                     "Residual_Market_Value": "number or null",
#                     "Total_Value": "number or null"
#                 },
#                 "Performance_Metrics": {
#                     "NAV_Gross": "number or null",
#                     "NAV_Net": "number or null",
#                     "Gross_IRR": "number or null",
#                     "Net_IRR": "number or null",
#                     "TVPI": "number or null",
#                     "DPI": "number or null",
#                     "RVPI": "number or null"
#                 }
#             },
#             "LP_Investor_Cashflows": [
#                 {
#                     "Transaction_Date": "string or null",
#                     "Investor_Name": "string or null",
#                     "Transaction_Type": "string or null",
#                     "Amount": "number or null",
#                     "Currency": "string or null",
#                     "Description": "string or null"
#                 }
#             ],
#             "Fund_Companies": [
#                 {
#                     "Company_Name": "string",
#                     "Industry": "string or null",
#                     "Headquarters_Country": "string or null",
#                     "Status": "string or null"
#                 }
#             ],
#             "Initial_Investments": [
#                 {
#                     "Company_Name": "string",
#                     "Investment_Date": "string or null",
#                     "Initial_Investment_Amount": "number or null",
#                     "Currency": "string or null",
#                     "Instrument_Type": "string or null"
#                 }
#             ],
#             "Company_Investment_Positions": [
#                 {
#                     "Company_Name": "string",
#                     "Committed_Capital": "number or null",
#                     "Invested_Capital": "number or null",
#                     "Current_Cost": "number or null",
#                     "Unrealized_Value": "number or null",
#                     "Total_Value": "number or null",
#                     "Gross_IRR": "number or null"
#                 }
#             ],
#             "Company_Valuation": [
#                 {
#                     "Company_Name": "string",
#                     "Valuation_Date": "string or null",
#                     "Enterprise_Value": "number or null",
#                     "Equity_Value": "number or null",
#                     "Ownership_Percentage": "number or null"
#                 }
#             ],
#             "Company_Financials": [
#                 {
#                     "Company_Name": "string",
#                     "Financial_Date": "string or null",
#                     "Revenue_LTM": "number or null",
#                     "EBITDA_LTM": "number or null",
#                     "Cash_Balance": "number or null",
#                     "Total_Debt": "number or null"
#                 }
#             ],
#             "Investment_History": [
#                 {
#                     "Company_Name": "string",
#                     "Transaction_Date": "string or null",
#                     "Transaction_Type": "string or null",
#                     "Transaction_Amount": "number or null",
#                     "Currency": "string or null"
#                 }
#             ],
#             "Reference_Values": {
#                 "Countries": ["string"],
#                 "Currencies": ["string"],
#                 "Industries": ["string"],
#                 "Instrument_Types": ["string"]
#             }
#         }

#     def _get_template_2_json_schema(self) -> Dict[str, Any]:
#         """Enhanced JSON schema for Template 2"""
#         return {
#             "Executive_Portfolio_Summary": {
#                 "General_Partner": {
#                     "GP_Name": "string or null",
#                     "GP_Contact": "string or null",
#                     "GP_Email": "string or null",
#                     "GP_Phone": "string or null"
#                 },
#                 "Portfolio_Overview": {
#                     "Assets_Under_Management": "number or null",
#                     "Number_of_Active_Funds": "number or null",
#                     "Number_of_Portfolio_Companies": "number or null",
#                     "Total_Capital_Invested": "number or null",
#                     "Total_Realized_Value": "number or null"
#                 },
#                 "Fund_Summary": {
#                     "Fund_Name": "string or null",
#                     "Fund_Currency": "string or null",
#                     "Total_Commitments": "number or null",
#                     "Total_Drawdowns": "number or null",
#                     "Remaining_Commitments": "number or null"
#                 },
#                 "Performance_Metrics": {
#                     "Total_Distributions": "number or null",
#                     "DPI": "number or null",
#                     "RVPI": "number or null",
#                     "TVPI": "number or null",
#                     "Net_IRR": "number or null"
#                 }
#             },
#             "Schedule_of_Investments": [
#                 {
#                     "Company_Name": "string",
#                     "Fund_Name": "string or null",
#                     "Reported_Date": "string or null",
#                     "Investment_Status": "string or null",
#                     "Security_Type": "string or null",
#                     "Ownership_Percentage": "number or null",
#                     "Initial_Investment_Date": "string or null",
#                     "Fund_Commitment": "number or null",
#                     "Total_Invested": "number or null",
#                     "Current_Cost": "number or null",
#                     "Reported_Value": "number or null",
#                     "Realized_Proceeds": "number or null"
#                 }
#             ],
#             "Statement_of_Operations": {
#                 "Revenue": {
#                     "Portfolio_Interest_Income": "number or null",
#                     "Portfolio_Dividend_Income": "number or null",
#                     "Other_Interest_Income": "number or null",
#                     "Total_Income": "number or null"
#                 },
#                 "Expenses": {
#                     "Management_Fees": "number or null",
#                     "Professional_Fees": "number or null",
#                     "Other_Expenses": "number or null",
#                     "Total_Expenses": "number or null"
#                 },
#                 "Net_Results": {
#                     "Net_Operating_Income": "number or null",
#                     "Realized_Gains_Losses": "number or null",
#                     "Unrealized_Gains_Losses": "number or null"
#                 }
#             },
#             "Statements_of_Cashflows": {
#                 "Operating_Activities": {
#                     "Purchase_of_Investments": "number or null",
#                     "Proceeds_from_Sales": "number or null",
#                     "Interest_Received": "number or null",
#                     "Net_Cash_from_Operations": "number or null"
#                 },
#                 "Financing_Activities": {
#                     "Capital_Contributions": "number or null",
#                     "Distributions_to_Investors": "number or null",
#                     "Net_Cash_from_Financing": "number or null"
#                 },
#                 "Net_Change": {
#                     "Net_Cash_Increase_Decrease": "number or null",
#                     "Beginning_Cash": "number or null",
#                     "Ending_Cash": "number or null"
#                 }
#             },
#             "PCAP_Statements": {
#                 "Beginning_Balance": {
#                     "Beginning_NAV": "number or null"
#                 },
#                 "Cash_Flows": {
#                     "Contributions": "number or null",
#                     "Distributions": "number or null"
#                 },
#                 "Fees_and_Expenses": {
#                     "Management_Fees": "number or null",
#                     "Other_Expenses": "number or null"
#                 },
#                 "Investment_Activity": {
#                     "Net_Investment_Income": "number or null",
#                     "Realized_Gains_Losses": "number or null",
#                     "Unrealized_Gains_Losses": "number or null"
#                 },
#                 "Ending_Balance": {
#                     "Ending_NAV": "number or null"
#                 }
#             },
#             "Portfolio_Companies_Profile": [
#                 {
#                     "Company_Name": "string",
#                     "Initial_Investment_Date": "string or null",
#                     "Industry": "string or null",
#                     "Headquarters": "string or null",
#                     "Company_Description": "string or null",
#                     "Business_Model": "string or null",
#                     "Fund_Ownership_Percentage": "number or null"
#                 }
#             ],
#             "Portfolio_Companies_Financials": [
#                 {
#                     "Company_Name": "string",
#                     "Reporting_Date": "string or null",
#                     "Revenue_LTM": "number or null",
#                     "EBITDA_LTM": "number or null",
#                     "Revenue_Growth_YoY": "number or null",
#                     "EBITDA_Margin": "number or null",
#                     "Enterprise_Value": "number or null",
#                     "Total_Debt": "number or null",
#                     "Cash_Balance": "number or null"
#                 }
#             ],
#             "FootNotes": {
#                 "Fund_Organization": {
#                     "Formation_Date": "string or null",
#                     "Legal_Structure": "string or null",
#                     "Governing_Law": "string or null"
#                 },
#                 "Accounting_Policies": {
#                     "Valuation_Methodology": "string or null",
#                     "Revenue_Recognition": "string or null"
#                 },
#                 "Risk_Factors": {
#                     "Market_Risks": "string or null",
#                     "Liquidity_Risks": "string or null"
#                 }
#             },
#             "Reference_Values": {
#                 "Industries": ["string"],
#                 "Currencies": ["string"],
#                 "Regions": ["string"],
#                 "Security_Types": ["string"]
#             }
#         }

#     def _get_template_1_specific_fields(self) -> Dict[str, Any]:
#         """Specific field guidance for Template 1"""
#         return {
#             "key_focus_areas": [
#                 "Fund structure and legal details",
#                 "Manager information and contact details", 
#                 "Detailed financial position with NAV, IRR metrics",
#                 "LP investor transactions and cashflows",
#                 "Portfolio company investments and positions",
#                 "Company-level financials and valuations",
#                 "Complete investment history",
#                 "Reference data for dropdowns"
#             ],
#             "financial_metrics": [
#                 "NAV (Net Asset Value)",
#                 "IRR (Internal Rate of Return)",
#                 "TVPI (Total Value to Paid-In)",
#                 "DPI (Distributions to Paid-In)", 
#                 "RVPI (Residual Value to Paid-In)",
#                 "Commitments and contributions",
#                 "Distributions and realized proceeds"
#             ],
#             "data_relationships": [
#                 "Fund Companies → Initial Investments → Company Investment Positions",
#                 "Investment History should include all transactions",
#                 "Company Valuation should match Company Financials dates",
#                 "LP Cashflows should reconcile with Fund Financial Position"
#             ]
#         }

#     def _get_template_2_specific_fields(self) -> Dict[str, Any]:
#         """Specific field guidance for Template 2"""
#         return {
#             "key_focus_areas": [
#                 "Executive summary and GP information",
#                 "Detailed schedule of investments",
#                 "Financial statements (Operations, Cashflows)",
#                 "PCAP (Partnership Capital Account) statements",
#                 "Portfolio company profiles and recent financials",
#                 "Footnotes and accounting disclosures",
#                 "Reference data for reporting"
#             ],
#             "financial_metrics": [
#                 "AUM (Assets Under Management)",
#                 "DPI, RVPI, TVPI multiples",
#                 "Net IRR performance",
#                 "Portfolio company financial metrics",
#                 "Cashflow statement reconciliation",
#                 "NAV changes in PCAP statements"
#             ],
#             "data_relationships": [
#                 "Schedule of Investments → Portfolio Companies Profile",
#                 "Statement of Operations → PCAP Statements",
#                 "Cashflows should balance with PCAP changes",
#                 "Footnotes should explain valuation methods"
#             ]
#         }

#     def _get_template_1_extraction_guidelines(self) -> str:
#         """Detailed extraction guidelines for Template 1"""
#         return """
#         EXTRACT PRIVATE EQUITY FUND DATA - TEMPLATE 1:

#         CRITICAL: This is a COMPREHENSIVE private equity fund template. You MUST extract:

#         1. FUND AND INVESTMENT VEHICLE INFORMATION:
#            - Fund name, legal structure, domicile, currency
#            - Fund size, total commitments, vintage year
#            - Key dates: inception, closing, investment period end
#            - Fee structure: management fee %, carried interest %, hurdle rate
#            - Investment focus: geography, sector, stage

#         2. FUND MANAGER:
#            - Management company name and contact details
#            - Office address, website, primary contact
#            - AUM, number of professionals, year founded

#         3. FINANCIAL POSITION:
#            - Commitment summary: total, paid-in, remaining
#            - Capital account: contributions, distributions, invested capital
#            - Performance: NAV (gross/net), IRR (gross/net), TVPI, DPI, RVPI
#            - Realized proceeds and residual market value

#         4. LP INVESTOR CASHFLOWS:
#            - All transactions with investors: contributions, distributions
#            - Dates, investor names, amounts, currencies
#            - Transaction types and descriptions

#         5. PORTFOLIO COMPANIES:
#            - All fund companies with industry and headquarters
#            - Company status (active, realized, etc.)
#            - Initial investment details: dates, amounts, instrument types
#            - Current investment positions: committed, invested, current cost
#            - Company valuations: enterprise value, equity value, ownership %

#         6. COMPANY FINANCIALS:
#            - Recent financial data: revenue LTM, EBITDA LTM
#            - Balance sheet items: cash, total debt
#            - Financial dates and periods

#         7. INVESTMENT HISTORY:
#            - Complete transaction history with companies
#            - Investment dates, types, amounts
#            - Include follow-on investments and exits

#         8. REFERENCE VALUES:
#            - Lists of countries, currencies, industries, instrument types

#         RULES:
#         - Extract ONLY explicit data from document
#         - Use null for missing data (never invent data)
#         - Format dates as YYYY-MM-DD
#         - Convert percentages to decimals (15% = 0.15)
#         - Maintain financial relationships and consistency
#         - Return valid JSON matching the exact schema
#         - Include ALL portfolio companies mentioned
#         """

#     def _get_template_2_extraction_guidelines(self) -> str:
#         """Detailed extraction guidelines for Template 2"""
#         return """
#         EXTRACT PORTFOLIO SUMMARY DATA - TEMPLATE 2:

#         CRITICAL: This is an EXECUTIVE PORTFOLIO SUMMARY template. You MUST extract:

#         1. EXECUTIVE PORTFOLIO SUMMARY:
#            - General Partner name and contact information
#            - Portfolio overview: AUM, number of funds, portfolio companies
#            - Fund summary: name, currency, commitments, drawdowns
#            - Performance metrics: distributions, DPI, RVPI, TVPI, Net IRR

#         2. SCHEDULE OF INVESTMENTS:
#            - Detailed list of all investments
#            - Company name, fund name, reported date
#            - Investment status, security type, ownership percentage
#            - Dates: initial investment and reporting
#            - Financials: commitment, total invested, current cost, reported value
#            - Realized proceeds from exits

#         3. FINANCIAL STATEMENTS:
#            - STATEMENT OF OPERATIONS:
#              * Revenue: portfolio interest, dividends, other income
#              * Expenses: management fees, professional fees, other
#              * Net results: operating income, realized/unrealized gains

#            - STATEMENTS OF CASHFLOWS:
#              * Operating: investment purchases, sales proceeds, interest
#              * Financing: contributions, distributions to investors
#              * Net change: cash balance changes

#         4. PCAP STATEMENTS (Partnership Capital Account):
#            - Beginning and ending NAV
#            - Cash flows: contributions and distributions
#            - Fees and expenses: management fees, other costs
#            - Investment activity: income, realized/unrealized gains

#         5. PORTFOLIO COMPANIES:
#            - Company profiles: description, business model, headquarters
#            - Financials: revenue, EBITDA, growth, margins, enterprise value
#            - Debt and cash positions

#         6. FOOTNOTES:
#            - Fund organization: formation, legal structure, governing law
#            - Accounting policies: valuation methods, revenue recognition
#            - Risk factors: market risks, liquidity risks

#         7. REFERENCE VALUES:
#            - Industries, currencies, regions, security types

#         RULES:
#         - Extract ONLY explicit data from document
#         - Use null for missing data (never invent data)
#         - Format dates as YYYY-MM-DD
#         - Maintain financial statement relationships
#         - Schedule of Investments should be comprehensive
#         - Footnotes should capture important disclosures
#         - Return valid JSON matching the exact schema
#         """

#     def process_texts(self, extracted_texts: List[Dict[str, Any]], template_id: int) -> Dict[str, Any]:
#         """
#         Process extracted texts with specified template - COMPLETE FIXED VERSION
#         """
#         self.usage_stats["total_requests"] += 1
        
#         try:
#             # Validate inputs
#             self._validate_inputs(extracted_texts, template_id)
            
#             # Get template configuration
#             template_config = self.template_configs.get(template_id)
#             if not template_config:
#                 raise ValueError(f"Invalid template_id: {template_id}")
            
#             logger.info(f"🧠 PROCESSING WITH TEMPLATE: {template_config['name']} (ID: {template_id})")
            
#             # Combine texts
#             combined_text = self._combine_texts(extracted_texts)
            
#             # Check cache with template-specific key
#             cache_key = self._generate_cache_key(combined_text, template_id)
#             if self.cache_enabled and cache_key in self.response_cache:
#                 logger.info(f"💾 Cache hit for template {template_id}")
#                 self.usage_stats["cache_hits"] += 1
#                 return self.response_cache[cache_key]
            
#             # Create template-specific prompt
#             prompt = self._create_template_specific_prompt(combined_text, template_config, template_id)
            
#             # Execute extraction with template validation
#             structured_data = self._execute_template_extraction(prompt, template_config, template_id)
            
#             # Add metadata
#             structured_data["_metadata"] = {
#                 "extraction_timestamp": datetime.now().isoformat(),
#                 "template_name": template_config['name'],
#                 "template_id": template_id,  # Ensure template ID is stored
#                 "template_version": template_config['version'],
#                 "processor_version": "2.3.0",
#                 "data_points": self._count_data_points(structured_data)
#             }
            
#             # Cache result with template-specific key
#             if self.cache_enabled:
#                 self.response_cache[cache_key] = structured_data
            
#             self.usage_stats["successful_extractions"] += 1
#             logger.info(f"✅ Successfully extracted {self._count_data_points(structured_data)} data points for template {template_id}")
            
#             return structured_data
            
#         except Exception as e:
#             self.usage_stats["failed_extractions"] += 1
#             logger.error(f"❌ LLM processing failed for template {template_id}: {str(e)}")
#             raise Exception(f"LLM processing failed for template {template_id}: {str(e)}")

#     def _validate_inputs(self, extracted_texts: List[Dict[str, Any]], template_id: int):
#         """Validate input parameters"""
#         if not extracted_texts:
#             raise ValueError("No extracted texts provided")
        
#         if template_id not in self.template_configs:
#             raise ValueError(f"Invalid template_id: {template_id}")

#     def _combine_texts(self, extracted_texts: List[Dict[str, Any]]) -> str:
#         """Combine extracted texts"""
#         texts = [text_data.get("text", "") for text_data in extracted_texts]
#         combined_text = "\n\n".join(texts)
        
#         # Less aggressive truncation for better extraction
#         if len(combined_text) > 25000:
#             combined_text = combined_text[:25000] + "... [text truncated for processing]"
        
#         return combined_text

#     def _generate_cache_key(self, text: str, template_id: int) -> str:
#         """Generate cache key"""
#         content = f"{text}_{template_id}"
#         return hashlib.md5(content.encode()).hexdigest()

#     def _create_template_specific_prompt(self, text: str, template_config: Dict[str, Any], template_id: int) -> str:
#         """Create template-specific prompt with strict instructions"""
#         schema_str = json.dumps(template_config["json_schema"], indent=2)
        
#         # Template-specific instructions
#         if template_id == 1:
#             template_specific_instruction = """
#             YOU ARE EXTRACTING DATA FOR TEMPLATE 1 - PRIVATE EQUITY FUND DETAILED TEMPLATE
#             Focus on: Fund details, manager information, financial positions, portfolio companies, investments
#             """
#         else:
#             template_specific_instruction = """
#             YOU ARE EXTRACTING DATA FOR TEMPLATE 2 - PORTFOLIO SUMMARY TEMPLATE  
#             Focus on: Executive summary, investment schedule, financial statements, company profiles
#             """
        
#         prompt = f"""
#         FINANCIAL DOCUMENT DATA EXTRACTION
        
#         TEMPLATE ID: {template_id}
#         TEMPLATE NAME: {template_config['name']}
        
#         {template_specific_instruction}
        
#         EXTRACTION GUIDELINES:
#         {template_config['extraction_guidelines']}
        
#         DOCUMENT TEXT:
#         {text}
        
#         REQUIRED JSON STRUCTURE:
#         {schema_str}
        
#         CRITICAL INSTRUCTIONS:
#         - Extract data specifically for TEMPLATE {template_id}
#         - Use null for missing data
#         - Format dates as YYYY-MM-DD
#         - Return ONLY valid JSON matching the exact structure above
#         - DO NOT include any explanations or additional text
#         - The JSON structure MUST match Template {template_id} requirements
        
#         RETURN VALID JSON:
#         """
        
#         return prompt

#     def _execute_template_extraction(self, prompt: str, template_config: Dict[str, Any], template_id: int) -> Dict[str, Any]:
#         """Execute extraction with template validation"""
#         for model_config in self.available_models:
#             model_name = model_config["name"]
            
#             try:
#                 logger.info(f"🤖 Trying model: {model_name} for template {template_id}")
                
#                 response = self.client.chat.completions.create(
#                     model=model_name,
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": f"You are a financial data extraction expert. You MUST extract data for Template {template_id}. Return ONLY valid JSON without any additional text."
#                         },
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ],
#                     temperature=0.1,
#                     max_tokens=8000,
#                     stream=False
#                 )
                
#                 result_text = response.choices[0].message.content
#                 structured_data = self._parse_response(result_text)
                
#                 # Enhanced validation to ensure template-specific data
#                 if self._validate_template_specific_data(structured_data, template_id):
#                     logger.info(f"✅ Model {model_name} produced valid data for template {template_id}")
#                     return structured_data
#                 else:
#                     logger.warning(f"⚠️ Model {model_name} produced invalid data for template {template_id}")
                    
#             except Exception as e:
#                 logger.warning(f"❌ Model {model_name} failed for template {template_id}: {e}")
#                 continue
        
#         # All models failed
#         raise Exception(f"All extraction attempts failed for template {template_id}")

#     def _validate_template_specific_data(self, data: Dict[str, Any], template_id: int) -> bool:
#         """Validate that data matches template requirements"""
#         if not data or not isinstance(data, dict):
#             return False
        
#         # Template-specific validation
#         if template_id == 1:
#             # Template 1 should have private equity specific fields
#             expected_fields = ['Fund_and_Investment_Vehicle_Information', 'Fund_Manager', 'Fund_Companies']
#             found_expected = any(field in data for field in expected_fields)
#         else:
#             # Template 2 should have portfolio summary specific fields  
#             expected_fields = ['Executive_Portfolio_Summary', 'Schedule_of_Investments', 'Statement_of_Operations']
#             found_expected = any(field in data for field in expected_fields)
        
#         return found_expected and self._count_data_points(data) >= 5

#     def _parse_response(self, response_text: str) -> Dict[str, Any]:
#         """Parse LLM response with enhanced error handling"""
#         try:
#             # Clean response text
#             cleaned_text = response_text.strip()
            
#             # Try direct JSON parsing first
#             try:
#                 return json.loads(cleaned_text)
#             except json.JSONDecodeError:
#                 pass
            
#             # Try to extract JSON from code blocks
#             json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned_text, re.DOTALL)
#             if json_match:
#                 try:
#                     return json.loads(json_match.group(1).strip())
#                 except json.JSONDecodeError:
#                     pass
            
#             # Try to find JSON between curly braces (more robust)
#             brace_match = re.search(r'\{[\s\S]*\}', cleaned_text)
#             if brace_match:
#                 try:
#                     return json.loads(brace_match.group(0))
#                 except json.JSONDecodeError:
#                     pass
            
#             # Last attempt: find any JSON-like structure
#             lines = cleaned_text.split('\n')
#             json_start = -1
#             json_end = -1
#             brace_count = 0
            
#             for i, line in enumerate(lines):
#                 if '{' in line and json_start == -1:
#                     json_start = i
#                     brace_count += line.count('{') - line.count('}')
#                 elif json_start != -1:
#                     brace_count += line.count('{') - line.count('}')
#                     if brace_count == 0:
#                         json_end = i + 1
#                         break
            
#             if json_start != -1 and json_end != -1:
#                 json_content = '\n'.join(lines[json_start:json_end])
#                 try:
#                     return json.loads(json_content)
#                 except json.JSONDecodeError:
#                     pass
            
#             raise ValueError("No valid JSON found in response")
            
#         except Exception as e:
#             logger.error(f"Response parsing failed: {e}")
#             logger.error(f"Response text: {response_text[:500]}...")
#             raise ValueError(f"Failed to parse response: {str(e)}")

#     def _count_data_points(self, data: Any) -> int:
#         """Count non-null data points"""
#         count = 0
        
#         def count_recursive(obj):
#             nonlocal count
#             if isinstance(obj, dict):
#                 for v in obj.values():
#                     count_recursive(v)
#             elif isinstance(obj, list):
#                 for item in obj:
#                     count_recursive(item)
#             elif obj is not None and obj != "":
#                 if isinstance(obj, str) and obj.strip() and obj.lower() not in ["null", "none", "n/a"]:
#                     count += 1
#                 elif not isinstance(obj, str):
#                     count += 1
        
#         count_recursive(data)
#         return count

#     def get_usage_statistics(self) -> Dict[str, Any]:
#         """Get usage statistics"""
#         return {
#             **self.usage_stats,
#             "cache_size": len(self.response_cache),
#             "timestamp": datetime.now().isoformat(),
#             "supported_templates": list(self.template_configs.keys())
#         }

#     def clear_cache(self):
#         """Clear response cache"""
#         self.response_cache.clear()
#         logger.info("Cache cleared")

#     def health_check(self) -> Dict[str, Any]:
#         """Health check"""
#         try:
#             test_response = self.client.chat.completions.create(
#                 model="llama-3.1-8b-instant",
#                 messages=[{"role": "user", "content": "Say 'OK'"}],
#                 max_tokens=10
#             )
            
#             return {
#                 "status": "healthy",
#                 "api_connectivity": "ok",
#                 "available_models": len(self.available_models),
#                 "supported_templates": len(self.template_configs)
#             }
            
#         except Exception as e:
#             return {
#                 "status": "unhealthy",
#                 "error": str(e)
#             }


# # Utility functions
# def create_llm_processor(cache_enabled: bool = True) -> LLMProcessor:
#     return LLMProcessor(cache_enabled=cache_enabled)

# def validate_template_id(template_id: int) -> bool:
#     return template_id in [1, 2]

# def get_supported_templates() -> Dict[int, str]:
#     processor = LLMProcessor()
#     return {tid: config["name"] for tid, config in processor.template_configs.items()}


# if __name__ == "__main__":
#     processor = LLMProcessor()
#     print("LLM Processor initialized")
#     print("Supported templates:", get_supported_templates())
#     print("Health check:", processor.health_check())
import json
import logging
import os
import re
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import hashlib
from groq import Groq
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class LLMProcessor:
    """
    Enhanced LLM Processor with detailed template-specific prompts
    """
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.response_cache = {}
        self.usage_stats = {
            "total_requests": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "cache_hits": 0
        }
        
        self._setup_environment()
        self._initialize_clients()
        self.template_configs = self._initialize_template_configs()
        
        logger.info("LLM Processor initialized successfully")

    def _setup_environment(self):
        """Setup environment variables"""
        try:
            possible_env_paths = [
                Path(__file__).parent.parent.parent / '.env',
                Path(__file__).parent / '.env',
                Path.cwd() / '.env',
            ]
            
            env_loaded = False
            for env_path in possible_env_paths:
                if env_path.exists():
                    load_dotenv(env_path)
                    logger.info(f"Loaded environment from: {env_path}")
                    env_loaded = True
                    break
            
            if not env_loaded:
                logger.warning("No .env file found, relying on system environment variables")
            
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
                
        except Exception as e:
            logger.error(f"Environment setup failed: {str(e)}")
            raise

    def _initialize_clients(self):
        """Initialize Groq client"""
        try:
            self.client = Groq(api_key=self.api_key)
            
            # Updated model list with better token limits
            self.available_models = [
                {
                    "name": "llama-3.3-70b-versatile",
                    "priority": 1,
                    "max_tokens": 4000,  # Reduced for rate limits
                    "context_window": 131072
                },
                {
                    "name": "llama-3.1-8b-instant", 
                    "priority": 2,
                    "max_tokens": 3000,  # Reduced for rate limits
                    "context_window": 131072
                },
                {
                    "name": "mixtral-8x7b-32768",
                    "priority": 3,
                    "max_tokens": 4000,
                    "context_window": 32768
                }
            ]
            
            logger.info(f"Initialized Groq client with {len(self.available_models)} models")
            
        except Exception as e:
            logger.error(f"Client initialization failed: {str(e)}")
            raise

    def _initialize_template_configs(self) -> Dict[int, Dict[str, Any]]:
        """Initialize detailed template configurations"""
        return {
            1: self._get_template_1_config(),
            2: self._get_template_2_config()
        }

    def _get_template_1_config(self) -> Dict[str, Any]:
        """Configuration for Template 1 - Private Equity Fund"""
        return {
            "name": "Private Equity Fund Detailed Template",
            "description": "Comprehensive private equity fund data extraction",
            "version": "1.3.0",
            "sheets": [
                "Fund and Investment Vehicle Information",
                "Fund Manager", 
                "Fund Investment Vehicle Financial Position",
                "LP Investor Cashflows",
                "Fund Companies",
                "Initial Investments",
                "Company Investment Positions", 
                "Company Valuation",
                "Company Financials",
                "Investment History",
                "Reference Values"
            ],
            "json_schema": self._get_template_1_json_schema(),
            "extraction_guidelines": self._get_template_1_extraction_guidelines(),
            "specific_fields": self._get_template_1_specific_fields()
        }

    def _get_template_2_config(self) -> Dict[str, Any]:
        """Configuration for Template 2 - Portfolio Summary"""
        return {
            "name": "Portfolio Summary Template",
            "description": "Executive portfolio summary and investment data",
            "version": "1.2.0",
            "sheets": [
                "Executive Portfolio Summary",
                "Schedule of Investments",
                "Statement of Operations", 
                "Statements of Cashflows",
                "PCAP Statements",
                "Portfolio Companies Profile",
                "Portfolio Companies Financials",
                "FootNotes",
                "Reference Values"
            ],
            "json_schema": self._get_template_2_json_schema(),
            "extraction_guidelines": self._get_template_2_extraction_guidelines(),
            "specific_fields": self._get_template_2_specific_fields()
        }

    def _get_template_1_json_schema(self) -> Dict[str, Any]:
        """Enhanced JSON schema for Template 1"""
        return {
            "Fund_and_Investment_Vehicle_Information": {
                "Fund_Details": {
                    "Fund_Name": "string or null",
                    "Fund_Currency": "string or null",
                    "Fund_Legal_Structure": "string or null",
                    "Fund_Domicile": "string or null",
                    "Fund_Size": "number or null",
                    "Total_Commitments": "number or null",
                    "Vintage_Year": "number or null",
                    "Financial_Year_End": "string or null"
                },
                "Key_Dates": {
                    "Inception_Date": "string or null",
                    "Final_Closing_Date": "string or null",
                    "Investment_Period_End_Date": "string or null"
                },
                "Fee_Structure": {
                    "Management_Fee_Rate": "number or null",
                    "Carried_Interest_Percentage": "number or null",
                    "Hurdle_Rate": "number or null"
                },
                "Investment_Focus": {
                    "Geography_Focus": "string or null",
                    "Sector_Focus": "string or null",
                    "Stage_Focus": "string or null"
                }
            },
            "Fund_Manager": {
                "Management_Company": {
                    "Management_Company_Name": "string or null",
                    "Manager_Website": "string or null",
                    "Primary_Contact": "string or null",
                    "Contact_Email": "string or null",
                    "Contact_Phone": "string or null",
                    "Office_Address": "string or null"
                },
                "Firm_Details": {
                    "Assets_Under_Management": "number or null",
                    "Number_of_Investment_Professionals": "number or null",
                    "Year_Founded": "number or null"
                }
            },
            "Fund_Investment_Vehicle_Financial_Position": {
                "Commitment_Summary": {
                    "Total_Commitment": "number or null",
                    "Paid_In_Capital": "number or null",
                    "Remaining_Commitment": "number or null"
                },
                "Capital_Account": {
                    "Total_Contributions": "number or null",
                    "Total_Distributions": "number or null",
                    "Invested_Capital": "number or null",
                    "Realized_Proceeds": "number or null",
                    "Residual_Market_Value": "number or null",
                    "Total_Value": "number or null"
                },
                "Performance_Metrics": {
                    "NAV_Gross": "number or null",
                    "NAV_Net": "number or null",
                    "Gross_IRR": "number or null",
                    "Net_IRR": "number or null",
                    "TVPI": "number or null",
                    "DPI": "number or null",
                    "RVPI": "number or null"
                }
            },
            "LP_Investor_Cashflows": [
                {
                    "Transaction_Date": "string or null",
                    "Investor_Name": "string or null",
                    "Transaction_Type": "string or null",
                    "Amount": "number or null",
                    "Currency": "string or null",
                    "Description": "string or null"
                }
            ],
            "Fund_Companies": [
                {
                    "Company_Name": "string",
                    "Industry": "string or null",
                    "Headquarters_Country": "string or null",
                    "Status": "string or null"
                }
            ],
            "Initial_Investments": [
                {
                    "Company_Name": "string",
                    "Investment_Date": "string or null",
                    "Initial_Investment_Amount": "number or null",
                    "Currency": "string or null",
                    "Instrument_Type": "string or null"
                }
            ],
            "Company_Investment_Positions": [
                {
                    "Company_Name": "string",
                    "Committed_Capital": "number or null",
                    "Invested_Capital": "number or null",
                    "Current_Cost": "number or null",
                    "Unrealized_Value": "number or null",
                    "Total_Value": "number or null",
                    "Gross_IRR": "number or null"
                }
            ],
            "Company_Valuation": [
                {
                    "Company_Name": "string",
                    "Valuation_Date": "string or null",
                    "Enterprise_Value": "number or null",
                    "Equity_Value": "number or null",
                    "Ownership_Percentage": "number or null"
                }
            ],
            "Company_Financials": [
                {
                    "Company_Name": "string",
                    "Financial_Date": "string or null",
                    "Revenue_LTM": "number or null",
                    "EBITDA_LTM": "number or null",
                    "Cash_Balance": "number or null",
                    "Total_Debt": "number or null"
                }
            ],
            "Investment_History": [
                {
                    "Company_Name": "string",
                    "Transaction_Date": "string or null",
                    "Transaction_Type": "string or null",
                    "Transaction_Amount": "number or null",
                    "Currency": "string or null"
                }
            ],
            "Reference_Values": {
                "Countries": ["string"],
                "Currencies": ["string"],
                "Industries": ["string"],
                "Instrument_Types": ["string"]
            }
        }

    def _get_template_2_json_schema(self) -> Dict[str, Any]:
        """Enhanced JSON schema for Template 2"""
        return {
            "Executive_Portfolio_Summary": {
                "General_Partner": {
                    "GP_Name": "string or null",
                    "GP_Contact": "string or null",
                    "GP_Email": "string or null",
                    "GP_Phone": "string or null"
                },
                "Portfolio_Overview": {
                    "Assets_Under_Management": "number or null",
                    "Number_of_Active_Funds": "number or null",
                    "Number_of_Portfolio_Companies": "number or null",
                    "Total_Capital_Invested": "number or null",
                    "Total_Realized_Value": "number or null"
                },
                "Fund_Summary": {
                    "Fund_Name": "string or null",
                    "Fund_Currency": "string or null",
                    "Total_Commitments": "number or null",
                    "Total_Drawdowns": "number or null",
                    "Remaining_Commitments": "number or null"
                },
                "Performance_Metrics": {
                    "Total_Distributions": "number or null",
                    "DPI": "number or null",
                    "RVPI": "number or null",
                    "TVPI": "number or null",
                    "Net_IRR": "number or null"
                }
            },
            "Schedule_of_Investments": [
                {
                    "Company_Name": "string",
                    "Fund_Name": "string or null",
                    "Reported_Date": "string or null",
                    "Investment_Status": "string or null",
                    "Security_Type": "string or null",
                    "Ownership_Percentage": "number or null",
                    "Initial_Investment_Date": "string or null",
                    "Fund_Commitment": "number or null",
                    "Total_Invested": "number or null",
                    "Current_Cost": "number or null",
                    "Reported_Value": "number or null",
                    "Realized_Proceeds": "number or null"
                }
            ],
            "Statement_of_Operations": {
                "Revenue": {
                    "Portfolio_Interest_Income": "number or null",
                    "Portfolio_Dividend_Income": "number or null",
                    "Other_Interest_Income": "number or null",
                    "Total_Income": "number or null"
                },
                "Expenses": {
                    "Management_Fees": "number or null",
                    "Professional_Fees": "number or null",
                    "Other_Expenses": "number or null",
                    "Total_Expenses": "number or null"
                },
                "Net_Results": {
                    "Net_Operating_Income": "number or null",
                    "Realized_Gains_Losses": "number or null",
                    "Unrealized_Gains_Losses": "number or null"
                }
            },
            "Statements_of_Cashflows": {
                "Operating_Activities": {
                    "Purchase_of_Investments": "number or null",
                    "Proceeds_from_Sales": "number or null",
                    "Interest_Received": "number or null",
                    "Net_Cash_from_Operations": "number or null"
                },
                "Financing_Activities": {
                    "Capital_Contributions": "number or null",
                    "Distributions_to_Investors": "number or null",
                    "Net_Cash_from_Financing": "number or null"
                },
                "Net_Change": {
                    "Net_Cash_Increase_Decrease": "number or null",
                    "Beginning_Cash": "number or null",
                    "Ending_Cash": "number or null"
                }
            },
            "PCAP_Statements": {
                "Beginning_Balance": {
                    "Beginning_NAV": "number or null"
                },
                "Cash_Flows": {
                    "Contributions": "number or null",
                    "Distributions": "number or null"
                },
                "Fees_and_Expenses": {
                    "Management_Fees": "number or null",
                    "Other_Expenses": "number or null"
                },
                "Investment_Activity": {
                    "Net_Investment_Income": "number or null",
                    "Realized_Gains_Losses": "number or null",
                    "Unrealized_Gains_Losses": "number or null"
                },
                "Ending_Balance": {
                    "Ending_NAV": "number or null"
                }
            },
            "Portfolio_Companies_Profile": [
                {
                    "Company_Name": "string",
                    "Initial_Investment_Date": "string or null",
                    "Industry": "string or null",
                    "Headquarters": "string or null",
                    "Company_Description": "string or null",
                    "Business_Model": "string or null",
                    "Fund_Ownership_Percentage": "number or null"
                }
            ],
            "Portfolio_Companies_Financials": [
                {
                    "Company_Name": "string",
                    "Reporting_Date": "string or null",
                    "Revenue_LTM": "number or null",
                    "EBITDA_LTM": "number or null",
                    "Revenue_Growth_YoY": "number or null",
                    "EBITDA_Margin": "number or null",
                    "Enterprise_Value": "number or null",
                    "Total_Debt": "number or null",
                    "Cash_Balance": "number or null"
                }
            ],
            "FootNotes": {
                "Fund_Organization": {
                    "Formation_Date": "string or null",
                    "Legal_Structure": "string or null",
                    "Governing_Law": "string or null"
                },
                "Accounting_Policies": {
                    "Valuation_Methodology": "string or null",
                    "Revenue_Recognition": "string or null"
                },
                "Risk_Factors": {
                    "Market_Risks": "string or null",
                    "Liquidity_Risks": "string or null"
                }
            },
            "Reference_Values": {
                "Industries": ["string"],
                "Currencies": ["string"],
                "Regions": ["string"],
                "Security_Types": ["string"]
            }
        }

    def _get_template_1_specific_fields(self) -> Dict[str, Any]:
        """Specific field guidance for Template 1"""
        return {
            "key_focus_areas": [
                "Fund structure and legal details",
                "Manager information and contact details", 
                "Detailed financial position with NAV, IRR metrics",
                "LP investor transactions and cashflows",
                "Portfolio company investments and positions",
                "Company-level financials and valuations",
                "Complete investment history",
                "Reference data for dropdowns"
            ],
            "financial_metrics": [
                "NAV (Net Asset Value)",
                "IRR (Internal Rate of Return)",
                "TVPI (Total Value to Paid-In)",
                "DPI (Distributions to Paid-In)", 
                "RVPI (Residual Value to Paid-In)",
                "Commitments and contributions",
                "Distributions and realized proceeds"
            ],
            "data_relationships": [
                "Fund Companies → Initial Investments → Company Investment Positions",
                "Investment History should include all transactions",
                "Company Valuation should match Company Financials dates",
                "LP Cashflows should reconcile with Fund Financial Position"
            ]
        }

    def _get_template_2_specific_fields(self) -> Dict[str, Any]:
        """Specific field guidance for Template 2"""
        return {
            "key_focus_areas": [
                "Executive summary and GP information",
                "Detailed schedule of investments",
                "Financial statements (Operations, Cashflows)",
                "PCAP (Partnership Capital Account) statements",
                "Portfolio company profiles and recent financials",
                "Footnotes and accounting disclosures",
                "Reference data for reporting"
            ],
            "financial_metrics": [
                "AUM (Assets Under Management)",
                "DPI, RVPI, TVPI multiples",
                "Net IRR performance",
                "Portfolio company financial metrics",
                "Cashflow statement reconciliation",
                "NAV changes in PCAP statements"
            ],
            "data_relationships": [
                "Schedule of Investments → Portfolio Companies Profile",
                "Statement of Operations → PCAP Statements",
                "Cashflows should balance with PCAP changes",
                "Footnotes should explain valuation methods"
            ]
        }

    def _get_template_1_extraction_guidelines(self) -> str:
        """Detailed extraction guidelines for Template 1"""
        return """
        EXTRACT PRIVATE EQUITY FUND DATA - TEMPLATE 1:

        CRITICAL: This is a COMPREHENSIVE private equity fund template. You MUST extract:

        1. FUND AND INVESTMENT VEHICLE INFORMATION:
           - Fund name, legal structure, domicile, currency
           - Fund size, total commitments, vintage year
           - Key dates: inception, closing, investment period end
           - Fee structure: management fee %, carried interest %, hurdle rate
           - Investment focus: geography, sector, stage

        2. FUND MANAGER:
           - Management company name and contact details
           - Office address, website, primary contact
           - AUM, number of professionals, year founded

        3. FINANCIAL POSITION:
           - Commitment summary: total, paid-in, remaining
           - Capital account: contributions, distributions, invested capital
           - Performance: NAV (gross/net), IRR (gross/net), TVPI, DPI, RVPI
           - Realized proceeds and residual market value

        4. LP INVESTOR CASHFLOWS:
           - All transactions with investors: contributions, distributions
           - Dates, investor names, amounts, currencies
           - Transaction types and descriptions

        5. PORTFOLIO COMPANIES:
           - All fund companies with industry and headquarters
           - Company status (active, realized, etc.)
           - Initial investment details: dates, amounts, instrument types
           - Current investment positions: committed, invested, current cost
           - Company valuations: enterprise value, equity value, ownership %

        6. COMPANY FINANCIALS:
           - Recent financial data: revenue LTM, EBITDA LTM
           - Balance sheet items: cash, total debt
           - Financial dates and periods

        7. INVESTMENT HISTORY:
           - Complete transaction history with companies
           - Investment dates, types, amounts
           - Include follow-on investments and exits

        8. REFERENCE VALUES:
           - Lists of countries, currencies, industries, instrument types

        RULES:
        - Extract ONLY explicit data from document
        - Use null for missing data (never invent data)
        - Format dates as YYYY-MM-DD
        - Convert percentages to decimals (15% = 0.15)
        - Maintain financial relationships and consistency
        - Return valid JSON matching the exact schema
        - Include ALL portfolio companies mentioned
        """

    def _get_template_2_extraction_guidelines(self) -> str:
        """Detailed extraction guidelines for Template 2"""
        return """
        EXTRACT PORTFOLIO SUMMARY DATA - TEMPLATE 2:

        CRITICAL: This is an EXECUTIVE PORTFOLIO SUMMARY template. You MUST extract:

        1. EXECUTIVE PORTFOLIO SUMMARY:
           - General Partner name and contact information
           - Portfolio overview: AUM, number of funds, portfolio companies
           - Fund summary: name, currency, commitments, drawdowns
           - Performance metrics: distributions, DPI, RVPI, TVPI, Net IRR

        2. SCHEDULE OF INVESTMENTS:
           - Detailed list of all investments
           - Company name, fund name, reported date
           - Investment status, security type, ownership percentage
           - Dates: initial investment and reporting
           - Financials: commitment, total invested, current cost, reported value
           - Realized proceeds from exits

        3. FINANCIAL STATEMENTS:
           - STATEMENT OF OPERATIONS:
             * Revenue: portfolio interest, dividends, other income
             * Expenses: management fees, professional fees, other
             * Net results: operating income, realized/unrealized gains

           - STATEMENTS OF CASHFLOWS:
             * Operating: investment purchases, sales proceeds, interest
             * Financing: contributions, distributions to investors
             * Net change: cash balance changes

        4. PCAP STATEMENTS (Partnership Capital Account):
           - Beginning and ending NAV
           - Cash flows: contributions and distributions
           - Fees and expenses: management fees, other costs
           - Investment activity: income, realized/unrealized gains

        5. PORTFOLIO COMPANIES:
           - Company profiles: description, business model, headquarters
           - Financials: revenue, EBITDA, growth, margins, enterprise value
           - Debt and cash positions

        6. FOOTNOTES:
           - Fund organization: formation, legal structure, governing law
           - Accounting policies: valuation methods, revenue recognition
           - Risk factors: market risks, liquidity risks

        7. REFERENCE VALUES:
           - Industries, currencies, regions, security types

        RULES:
        - Extract ONLY explicit data from document
        - Use null for missing data (never invent data)
        - Format dates as YYYY-MM-DD
        - Maintain financial statement relationships
        - Schedule of Investments should be comprehensive
        - Footnotes should capture important disclosures
        - Return valid JSON matching the exact schema
        """

    def process_texts(self, extracted_texts: List[str], template_id: int) -> Dict[str, Any]:
        """
        Process extracted texts with specified template - FIXED VERSION
        """
        self.usage_stats["total_requests"] += 1
        
        try:
            # Validate inputs
            self._validate_inputs(extracted_texts, template_id)
            
            # Get template configuration
            template_config = self.template_configs.get(template_id)
            if not template_config:
                raise ValueError(f"Invalid template_id: {template_id}")
            
            logger.info(f"🧠 PROCESSING WITH TEMPLATE: {template_config['name']} (ID: {template_id})")
            
            # Combine texts - FIXED: Handle both strings and dictionaries
            combined_text = self._combine_texts(extracted_texts)
            
            # Check cache with template-specific key
            cache_key = self._generate_cache_key(combined_text, template_id)
            if self.cache_enabled and cache_key in self.response_cache:
                logger.info(f"💾 Cache hit for template {template_id}")
                self.usage_stats["cache_hits"] += 1
                return self.response_cache[cache_key]
            
            # Create template-specific prompt with text optimization
            prompt = self._create_optimized_prompt(combined_text, template_config, template_id)
            
            # Execute extraction with template validation and rate limit handling
            structured_data = self._execute_extraction_with_retry(prompt, template_config, template_id)
            
            # Add metadata
            structured_data["_metadata"] = {
                "extraction_timestamp": datetime.now().isoformat(),
                "template_name": template_config['name'],
                "template_id": template_id,
                "template_version": template_config['version'],
                "processor_version": "2.3.0",
                "data_points": self._count_data_points(structured_data)
            }
            
            # Cache result with template-specific key
            if self.cache_enabled:
                self.response_cache[cache_key] = structured_data
            
            self.usage_stats["successful_extractions"] += 1
            logger.info(f"✅ Successfully extracted {self._count_data_points(structured_data)} data points for template {template_id}")
            
            return structured_data
            
        except Exception as e:
            self.usage_stats["failed_extractions"] += 1
            logger.error(f"❌ LLM processing failed for template {template_id}: {str(e)}")
            raise Exception(f"LLM processing failed for template {template_id}: {str(e)}")

    def _validate_inputs(self, extracted_texts: List[str], template_id: int):
        """Validate input parameters - FIXED: Accept list of strings"""
        if not extracted_texts:
            raise ValueError("No extracted texts provided")
        
        if template_id not in self.template_configs:
            raise ValueError(f"Invalid template_id: {template_id}")

    def _combine_texts(self, extracted_texts: List[str]) -> str:
        """Combine extracted texts - FIXED: Handle list of strings"""
        # Handle both strings and dictionaries for backward compatibility
        texts = []
        for text_item in extracted_texts:
            if isinstance(text_item, dict):
                # If it's a dictionary, extract the text field
                text = text_item.get("text", "")
            else:
                # If it's already a string, use it directly
                text = text_item
            texts.append(text)
        
        combined_text = "\n\n".join(texts)
        
        # More aggressive truncation for rate limits
        if len(combined_text) > 15000:
            logger.warning(f"⚠️ Text too long ({len(combined_text)} chars), truncating to 15000")
            combined_text = combined_text[:15000] + "... [text truncated for rate limits]"
        
        logger.info(f"📝 Combined text length: {len(combined_text)} characters")
        return combined_text

    def _generate_cache_key(self, text: str, template_id: int) -> str:
        """Generate cache key"""
        content = f"{text}_{template_id}"
        return hashlib.md5(content.encode()).hexdigest()

    def _create_optimized_prompt(self, text: str, template_config: Dict[str, Any], template_id: int) -> str:
        """Create optimized prompt with reduced token usage"""
        # Use simplified schema for token efficiency
        simplified_schema = self._get_simplified_schema(template_id)
        schema_str = json.dumps(simplified_schema, indent=2)
        
        # Template-specific instructions
        if template_id == 1:
            template_specific_instruction = """
            YOU ARE EXTRACTING DATA FOR TEMPLATE 1 - PRIVATE EQUITY FUND DETAILED TEMPLATE
            Focus on: Fund details, manager information, financial positions, portfolio companies, investments
            """
        else:
            template_specific_instruction = """
            YOU ARE EXTRACTING DATA FOR TEMPLATE 2 - PORTFOLIO SUMMARY TEMPLATE  
            Focus on: Executive summary, investment schedule, financial statements, company profiles
            """
        
        # Simplified guidelines for token efficiency
        simplified_guidelines = self._get_simplified_guidelines(template_id)
        
        prompt = f"""
        FINANCIAL DOCUMENT DATA EXTRACTION
        
        TEMPLATE ID: {template_id}
        TEMPLATE NAME: {template_config['name']}
        
        {template_specific_instruction}
        
        EXTRACTION GUIDELINES:
        {simplified_guidelines}
        
        DOCUMENT TEXT:
        {text}
        
        REQUIRED JSON STRUCTURE:
        {schema_str}
        
        CRITICAL INSTRUCTIONS:
        - Extract data specifically for TEMPLATE {template_id}
        - Use null for missing data
        - Format dates as YYYY-MM-DD
        - Return ONLY valid JSON matching the exact structure above
        - DO NOT include any explanations or additional text
        - The JSON structure MUST match Template {template_id} requirements
        
        RETURN VALID JSON:
        """
        
        logger.info(f"📝 Prompt length: {len(prompt)} characters")
        return prompt

    def _get_simplified_schema(self, template_id: int) -> Dict[str, Any]:
        """Get simplified schema to reduce token usage"""
        if template_id == 1:
            return {
                "Fund_and_Investment_Vehicle_Information": {
                    "Fund_Details": {
                        "Fund_Name": "string or null",
                        "Fund_Currency": "string or null",
                        "Fund_Size": "number or null",
                        "Total_Commitments": "number or null"
                    }
                },
                "Fund_Manager": {
                    "Management_Company": {
                        "Management_Company_Name": "string or null"
                    }
                },
                "Fund_Investment_Vehicle_Financial_Position": {
                    "Performance_Metrics": {
                        "NAV_Gross": "number or null",
                        "Gross_IRR": "number or null",
                        "TVPI": "number or null"
                    }
                },
                "Fund_Companies": [
                    {
                        "Company_Name": "string",
                        "Industry": "string or null"
                    }
                ]
            }
        else:
            return {
                "Executive_Portfolio_Summary": {
                    "Portfolio_Overview": {
                        "Assets_Under_Management": "number or null",
                        "Number_of_Portfolio_Companies": "number or null"
                    }
                },
                "Schedule_of_Investments": [
                    {
                        "Company_Name": "string",
                        "Total_Invested": "number or null",
                        "Reported_Value": "number or null"
                    }
                ]
            }

    def _get_simplified_guidelines(self, template_id: int) -> str:
        """Get simplified guidelines to reduce token usage"""
        if template_id == 1:
            return """
            Extract key private equity fund data:
            - Fund name, currency, size, commitments
            - Management company name
            - Performance metrics: NAV, IRR, TVPI
            - Portfolio companies with names and industries
            Use null for missing data. Return valid JSON.
            """
        else:
            return """
            Extract key portfolio summary data:
            - Assets under management, portfolio company count
            - Investment schedule with company names and values
            Use null for missing data. Return valid JSON.
            """

    def _execute_extraction_with_retry(self, prompt: str, template_config: Dict[str, Any], template_id: int) -> Dict[str, Any]:
        """Execute extraction with retry logic for rate limits"""
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            for model_config in self.available_models:
                model_name = model_config["name"]
                
                try:
                    logger.info(f"🤖 Attempt {attempt + 1}: Trying model {model_name} for template {template_id}")
                    
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": f"You are a financial data extraction expert. Extract data for Template {template_id}. Return ONLY valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.1,
                        max_tokens=model_config["max_tokens"],
                        stream=False
                    )
                    
                    result_text = response.choices[0].message.content
                    structured_data = self._parse_response(result_text)
                    
                    # Enhanced validation to ensure template-specific data
                    if self._validate_template_specific_data(structured_data, template_id):
                        logger.info(f"✅ Model {model_name} produced valid data for template {template_id}")
                        return structured_data
                    else:
                        logger.warning(f"⚠️ Model {model_name} produced invalid data for template {template_id}")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "rate_limit" in error_msg or "413" in error_msg or "429" in error_msg:
                        logger.warning(f"⏰ Rate limit hit for {model_name}, waiting {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        break  # Break to retry with same model
                    else:
                        logger.warning(f"❌ Model {model_name} failed for template {template_id}: {e}")
                        continue
        
        # All models and retries failed
        raise Exception(f"All extraction attempts failed for template {template_id} after {max_retries} retries")

    def _validate_template_specific_data(self, data: Dict[str, Any], template_id: int) -> bool:
        """Validate that data matches template requirements"""
        if not data or not isinstance(data, dict):
            return False
        
        # More lenient validation for rate-limited scenarios
        if template_id == 1:
            # Template 1 should have some private equity fields
            expected_fields = ['Fund_and_Investment_Vehicle_Information', 'Fund_Manager', 'Fund_Companies']
            found_expected = any(field in data for field in expected_fields)
        else:
            # Template 2 should have some portfolio summary fields  
            expected_fields = ['Executive_Portfolio_Summary', 'Schedule_of_Investments']
            found_expected = any(field in data for field in expected_fields)
        
        return found_expected and self._count_data_points(data) >= 3  # Reduced threshold

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response with enhanced error handling"""
        try:
            # Clean response text
            cleaned_text = response_text.strip()
            
            # Try direct JSON parsing first
            try:
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                pass
            
            # Try to extract JSON from code blocks
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1).strip())
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON between curly braces (more robust)
            brace_match = re.search(r'\{[\s\S]*\}', cleaned_text)
            if brace_match:
                try:
                    return json.loads(brace_match.group(0))
                except json.JSONDecodeError:
                    pass
            
            # Last attempt: find any JSON-like structure
            lines = cleaned_text.split('\n')
            json_start = -1
            json_end = -1
            brace_count = 0
            
            for i, line in enumerate(lines):
                if '{' in line and json_start == -1:
                    json_start = i
                    brace_count += line.count('{') - line.count('}')
                elif json_start != -1:
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_start != -1 and json_end != -1:
                json_content = '\n'.join(lines[json_start:json_end])
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass
            
            # Fallback: return minimal valid structure
            logger.warning("⚠️ No valid JSON found, returning fallback structure")
            return {"error": "No structured data extracted", "raw_response": cleaned_text[:500]}
            
        except Exception as e:
            logger.error(f"Response parsing failed: {e}")
            logger.error(f"Response text: {response_text[:500]}...")
            return {"error": f"Failed to parse response: {str(e)}"}

    def _count_data_points(self, data: Any) -> int:
        """Count non-null data points"""
        count = 0
        
        def count_recursive(obj):
            nonlocal count
            if isinstance(obj, dict):
                for v in obj.values():
                    count_recursive(v)
            elif isinstance(obj, list):
                for item in obj:
                    count_recursive(item)
            elif obj is not None and obj != "":
                if isinstance(obj, str) and obj.strip() and obj.lower() not in ["null", "none", "n/a"]:
                    count += 1
                elif not isinstance(obj, str):
                    count += 1
        
        count_recursive(data)
        return count

    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            **self.usage_stats,
            "cache_size": len(self.response_cache),
            "timestamp": datetime.now().isoformat(),
            "supported_templates": list(self.template_configs.keys())
        }

    def clear_cache(self):
        """Clear response cache"""
        self.response_cache.clear()
        logger.info("Cache cleared")

    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        try:
            test_response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=10
            )
            
            return {
                "status": "healthy",
                "api_connectivity": "ok",
                "available_models": len(self.available_models),
                "supported_templates": len(self.template_configs)
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Utility functions
def create_llm_processor(cache_enabled: bool = True) -> LLMProcessor:
    return LLMProcessor(cache_enabled=cache_enabled)

def validate_template_id(template_id: int) -> bool:
    return template_id in [1, 2]

def get_supported_templates() -> Dict[int, str]:
    processor = LLMProcessor()
    return {tid: config["name"] for tid, config in processor.template_configs.items()}


if __name__ == "__main__":
    processor = LLMProcessor()
    print("LLM Processor initialized")
    print("Supported templates:", get_supported_templates())
    print("Health check:", processor.health_check())