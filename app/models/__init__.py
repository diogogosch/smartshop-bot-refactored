"""Models package - Exports all database models."""
from app.models.shopping import ShoppingItem
from app.models.user import User

__all__ = [
    "ShoppingItem",
    "User",
]
