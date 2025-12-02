"""Input validation utilities for SmartShopBot."""
from typing import Tuple

class Validators:
    """Centralized input validation."""
    
    @staticmethod
    def validate_item_name(name: str) -> Tuple[bool, str]:
        """Validate shopping item name.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or len(name.strip()) == 0:
            return False, "Item name cannot be empty"
        if len(name) > 255:
            return False, "Item name too long (max 255 chars)"
        if any(char in name for char in ['\n', '\t', '\r']):
            return False, "Item name contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_quantity(qty: str) -> Tuple[bool, str]:
        """Validate quantity format."""
        if not qty:
            return True, ""
        if len(qty) > 50:
            return False, "Quantity too long (max 50 chars)"
        return True, ""
    
    @staticmethod
    def validate_currency_code(code: str) -> Tuple[bool, str]:
        """Validate ISO currency code."""
        valid_codes = {"USD", "EUR", "BRL", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR"}
        if code.upper() not in valid_codes:
            return False, f"Invalid currency: {code}"
        return True, ""
    
    @staticmethod
    def validate_language_code(code: str) -> Tuple[bool, str]:
        """Validate language code."""
        valid_langs = {"en", "pt", "es", "fr", "de", "it", "ja", "zh", "ru", "ar"}
        if code.lower() not in valid_langs:
            return False, f"Invalid language: {code}"
        return True, ""

validators = Validators()
