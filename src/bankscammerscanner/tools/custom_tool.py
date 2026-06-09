from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re

class SSIRCheckerInput(BaseModel):
    """Input schema for SG_SSIR_Checker."""
    sender_id: str = Field(..., description="The SMS sender name or phone number to verify.")

class SGSSIRChecker(BaseTool):
    name: str = "SG_SSIR_Checker"
    description: str = (
        "Verifies if a sender ID or phone number is registered under Singapore's SMS Sender ID Registry (SSIR). "
        "Use this when you have a phone number or alphanumeric name (e.g., +65... or 'DBS') to catch impersonation."
    )
    args_schema: Type[BaseModel] = SSIRCheckerInput

    VERIFIED_SENDER_IDS: dict = {
        "DBS": "DBS Bank",
        "POSB": "POSB (DBS Bank)",
        "OCBC": "OCBC Bank",
        "UOB": "United Overseas Bank",
        "Maybank": "Maybank Singapore",
        "SCB": "Standard Chartered Bank",
        "StanChart": "Standard Chartered Bank",
        "HSBC": "HSBC Singapore",
        "Citibank": "Citibank Singapore",
        "Citi": "Citibank Singapore",
        "BOC": "Bank of China Singapore",
        "MAS": "Monetary Authority of Singapore",
        "CPF": "Central Provident Fund Board",
        "IRAS": "Inland Revenue Authority of Singapore",
        "MOH": "Ministry of Health",
        "SPF": "Singapore Police Force",
    }

    def _run(self, sender_id: str) -> str:
        clean_id = sender_id.replace(" ", "").replace("-", "")
        sg_mobile_pattern = r'^(\+65)?[89]\d{7}$'
        foreign_mobile_pattern = r'^\+(?!65)\d{7,15}$'

        if "Likely-SCAM" in sender_id:
            return "CRITICAL: Flagged by IMDA as 'Likely-SCAM'."
        if re.match(sg_mobile_pattern, clean_id):
            return "NOTICE: Personal Singapore mobile number used as sender. If the message claims to be from a bank or financial institution, this is a spoofing attempt. Non-financial businesses (clinics, shops, etc.) may legitimately use personal numbers."
        if re.match(foreign_mobile_pattern, clean_id):
            country_code = clean_id[1:3]
            return f"WARNING: Foreign mobile number (+{country_code}...) contacting about Singapore financial matters. Legitimate Singapore banks never contact customers from foreign numbers."
        if len(sender_id) > 11 and not sender_id.startswith('+'):
            return "SUSPICIOUS: The Sender ID is unusually long for a registered corporate alpha-tag."

        if sender_id.strip() in self.VERIFIED_SENDER_IDS:
            institution = self.VERIFIED_SENDER_IDS[sender_id.strip()]
            return f"VERIFIED: '{sender_id}' is a known registered sender ID for {institution}. Sender ID is legitimate — focus analysis on message content."

        return "UNVERIFIED: Sender ID is alphanumeric but not in the known whitelist of registered Singapore institutions. Treat with caution and weight linguistic analysis heavily."
    
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

        if 'wa.me' in url_lower or 'whatsapp.com' in url_lower:
            return "WARNING: WhatsApp contact link detected. Legitimate banks never use WhatsApp as an official contact channel."
        if 'weixin.com' in url_lower or 'wechat.com' in url_lower:
            return "WARNING: WeChat contact link detected. Legitimate banks never use WeChat as an official contact channel."
        if 't.me' in url_lower or 'telegram.me' in url_lower:
            return "WARNING: Telegram link detected. Legitimate banks never use Telegram as an official contact channel."

        if any(tld in url_lower for tld in suspicious_tlds):
            return f"HIGH RISK: Suspicious domain extension detected in {url}."

        banks = {"dbs": "dbs.com.sg", "ocbc": "ocbc.com", "uob": "uobgroup.com"}
        for bank, official in banks.items():
            if bank in url_lower and official not in url_lower:
                return f"PHISHING ALERT: URL contains '{bank}' but is not the official domain '{official}'."

        if re.match(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_lower):
            return "CRITICAL: Link uses a raw IP address. This is a definitive hallmark of a scam site."

        return "Technical Check: URL structure appears standard."
