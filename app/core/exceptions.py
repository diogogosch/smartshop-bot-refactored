"""Custom exception classes for the shopping bot application."""

class SmartShopException(Exception):
    """Base exception for all SmartShop related errors."""
    pass

class DatabaseException(SmartShopException):
    """Raised when a database operation fails."""
    pass

class UserNotFound(SmartShopException):
    """Raised when a user is not found in the database."""
    pass

class ShoppingListException(SmartShopException):
    """Raised when shopping list operation fails."""
    pass

class OCRException(SmartShopException):
    """Raised when OCR processing fails."""
    pass

class ValidationException(SmartShopException):
    """Raised when data validation fails."""
    pass

class NotificationException(SmartShopException):
    """Raised when notification sending fails."""
    pass
