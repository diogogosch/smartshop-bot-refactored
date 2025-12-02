"""Base handler class for Telegram bot handlers"""
import logging
from typing import Any, Optional
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class BaseHandler:
    """Base class for all command handlers"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE, error: Exception) -> None:
        """Handle errors uniformly"""
        self.logger.error(f"Error in {self.__class__.__name__}: {str(error)}")
        if update and update.effective_chat:
            try:
                await update.effective_chat.send_message(
                    "❌ An error occurred. Please try again later."
                )
            except Exception as e:
                self.logger.error(f"Error sending error message: {e}")
    
    def get_user_id(self, update: Update) -> Optional[int]:
        """Extract user ID from update"""
        return update.effective_user.id if update.effective_user else None
    
    def get_chat_id(self, update: Update) -> Optional[int]:
        """Extract chat ID from update"""
        return update.effective_chat.id if update.effective_chat else None
    
    def get_username(self, update: Update) -> Optional[str]:
        """Extract username from update"""
        return update.effective_user.username if update.effective_user else None
