"""Utility helper functions for SmartShopBot."""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

class Helpers:
    """General utility functions."""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format amount as currency string."""
        return f"{currency} {amount:.2f}"
    
    @staticmethod
    def parse_quantity_and_unit(qty_str: str) -> tuple:
        """Parse quantity string into amount and unit.
        
        Example: '2L' -> (2.0, 'L'), '500g' -> (500.0, 'g')
        """
        qty_str = qty_str.strip()
        match = re.match(r'([\d.]+)\s*(.*?)$', qty_str)
        if match:
            try:
                amount = float(match.group(1))
                unit = match.group(2) or ""
                return amount, unit
            except ValueError:
                pass
        return 1, qty_str
    
    @staticmethod
    def format_shopping_list(items: List[Dict[str, Any]]) -> str:
        """Format shopping list for display in Telegram."""
        if not items:
            return "📝 Your shopping list is empty"
        
        text = "📝 **Your Shopping List:**\n"
        for idx, item in enumerate(items, 1):
            qty = f" ({item.get('quantity', '')})" if item.get('quantity') else ""
            text += f"{idx}. {item.get('name', 'Unknown')}{qty}\n"
        text += f"\n**Total Items:** {len(items)}"
        return text
    
    @staticmethod
    def get_time_period_range(period: str = "day") -> tuple:
        """Get date range for analytics period.
        
        Args:
            period: 'today', 'week', 'month', or 'year'
        
        Returns:
            Tuple of (start_datetime, end_datetime)
        """
        now = datetime.now()
        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "week":
            start = now - timedelta(days=7)
            end = now
        elif period == "month":
            start = now - timedelta(days=30)
            end = now
        elif period == "year":
            start = now - timedelta(days=365)
            end = now
        else:
            start = now - timedelta(days=1)
            end = now
        return start, end
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to max length with suffix."""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

helpers = Helpers()
