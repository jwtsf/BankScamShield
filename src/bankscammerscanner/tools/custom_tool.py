from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re

# 1. Define the "Schema" (What the tool expects to receive)
class SSIRCheckerInput(BaseModel):
    """Input schema for SG_SSIR_Checker."""
    sender_id: str = Field(..., description="The SMS sender name or phone number to verify.")

# 2. Define the Tool Class
class SGSSIRChecker(BaseTool):
    name: str = "SG_SSIR_Checker"
    description: str = (
        "Useful for verifying if a sender ID or phone number complies with "
        "Singapore's SMS Sender ID Registry. Use this to catch impersonation."
        """
        Checks if a sender ID follows Singapore's SMS Sender ID Registry (SSIR) rules.
        Use this when you have a phone number or alphanumeric name (e.g., +65... or 'DBS').
        """
    )
    args_schema: Type[BaseModel] = SSIRCheckerInput

    def _run(self, sender_id: str) -> str:
        # Implementation logic
        clean_id = sender_id.replace(" ", "").replace("-", "")
        mobile_pattern = r'^(\+65)?[89]\d{7}$'
        
        if "Likely-SCAM" in sender_id:
            return "CRITICAL: Flagged by IMDA as 'Likely-SCAM'."
        if re.match(mobile_pattern, clean_id):
            return "WARNING: Personal mobile number used for bank alert (Spoofing)."
        if len(sender_id) > 11 and not sender_id.startswith('+'):
            return "SUSPICIOUS: The Sender ID is unusually long for a registered corporate alpha-tag."
        
        return "Neutral: Sender ID is alphanumeric and potentially registered. Proceed with linguistic check."
    
class URLAnalyserInput(BaseModel):
    """Input schema for URL analysis tool."""
    url: str = Field(..., description="The full URL link found within the message body.")


class URLTechnicalAnalyser(BaseTool):
    name: str = "URL_Technical_Analyser"
    description: str = (
        "Analyzes a URL for technical red flags like typosquatting, "
        "suspicious domain extensions, or raw IP addresses."
    )

    args_schema: Type[BaseModel] = URLAnalyserInput

    def _run(self, url: str) -> str:
            url_lower = url.lower()
            suspicious_tlds = ['.xyz', '.top', '.site', '.click', '.info', '.zip']
            
            # Check for suspicious TLDs
            if any(tld in url_lower for tld in suspicious_tlds):
                return f"HIGH RISK: Suspicious domain extension detected in {url}."
            
            # Check for Bank Typosquatting
            banks = {"dbs": "dbs.com.sg", "ocbc": "ocbc.com", "uob": "uobgroup.com"}
            for bank, official in banks.items():
                if bank in url_lower and official not in url_lower:
                    return f"PHISHING ALERT: URL contains '{bank}' but is not the official domain '{official}'."
            
            # Check for Raw IP Address
            if re.match(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_lower):
                return "CRITICAL: Link uses a raw IP address. This is a definitive hallmark of a scam site."
                
            return "Technical Check: URL structure appears standard."   

# Repeat similar structure for URL_Deep_Link_Analyzer...