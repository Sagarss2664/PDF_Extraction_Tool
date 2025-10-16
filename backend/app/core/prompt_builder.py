def build_prompt(template_id: str, text: str) -> str:
    if template_id == "template1":
        return f"""
You are a financial document parser. Extract the following fields from the text below according to Template 1:

- Fund Name, Currency, Size, Vintage Year
- GP Commitment and %
- Investment Structure, Legal Structure
- Investment Vehicle Contributions, Distributions, NAV
- IRR, TVPI, DPI, RVPI
- LP Cashflows: Contributions, Distributions, Valuations
- Fund Companies: Name, Sector, Country, Description
- Initial Investments: Date, Instrument, Amount, Ownership %
- Company Financials: Revenue, EBITDA, Debt, IRR

Return a JSON object with these fields grouped by section.

--- BEGIN TEXT ---
{text}
--- END TEXT ---
"""
    elif template_id == "template2":
        return f"""
You are a private equity report parser. Extract the following fields from the text below according to Template 2:

- Executive Summary: Reporting Date, AUM, Active Funds, DPI, RVPI, TVPI
- Schedule of Investments: Company, Fund, Investment Status, Security Type, Shares, Ownership %, Invested, Valuation, IRR
- Statement of Operations: Income, Expenses, Net Operating Income, Realized/Unrealized Gains
- Cashflows: Contributions, Distributions, Net Cash Flow
- PCAP Statement: NAV, Commitments, Fees, IRR
- Portfolio Company Profile: Name, Industry, Description, Ownership %, Valuation
- Portfolio Financials: Revenue, EBITDA, Debt, TEV, Multiples

Return a JSON object with these fields grouped by section.

--- BEGIN TEXT ---
{text}
--- END TEXT ---
"""
    else:
        raise ValueError("Unknown template ID")