import re
from typing import List, Pattern

class PiiRedactor:
    """Processor to detect and redact/replace PII (Personally Identifiable Information)"""
    
    # Simple regex patterns
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    # Phone numbers (simplified: e.g. 03-1234-5678, 090-1234-5678)
    # Allows valid formats with or without hyphens
    PHONE_PATTERN = re.compile(r'(\d{2,4}[-\(]\d{2,4}[-\)]\d{3,4})|(\d{10,11})')
    
    # Credit cards (simplified: 12-19 digits)
    # Does not perform Luhn algorithm check
    CREDIT_CARD_PATTERN = re.compile(r'\b(?:\d[ -]*?){13,16}\b')

    @classmethod
    def redact(cls, text: str, replace_text: str = "[REDACTED]") -> str:
        """Redact or replace PII in text
        
        Args:
            text (str): Target text
            replace_text (str): Replacement string
            
        Returns:
            str: Redacted text
        """
        text = cls.EMAIL_PATTERN.sub(replace_text, text)
        text = cls.PHONE_PATTERN.sub(replace_text, text)
        text = cls.CREDIT_CARD_PATTERN.sub(replace_text, text)
        return text
