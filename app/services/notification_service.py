import logging
from typing import Optional
from telegram import Bot

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot: Optional[Bot] = None):
        self.bot = bot
    
    async def send(self, chat_id: int, msg: str, parse: str = "HTML") -> bool:
        try:
            if not self.bot:
                return False
            await self.bot.send_message(chat_id, msg, parse_mode=parse)
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    async def daily_reminder(self, chat_id: int) -> bool:
        msg = "📝 Check your shopping list: /list"
        return await self.send(chat_id, msg)
    
    async def price_alert(self, chat_id: int, item: str, new_price: float) -> bool:
        msg = f"📈 Price update: {item} - R${new_price:.2f}"
        return await self.send(chat_id, msg)

notification_service = NotificationService()
