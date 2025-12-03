import logging
from telegram.ext import Application, CommandHandler
from app.config.settings import settings
from app.core.database import init_db
from app.handlers.shopping_handler import (
    add_item_handler, 
    list_handler, 
    clear_handler, 
    suggestions_handler
)

# Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.LOG_LEVEL
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting SmartShopBot...")
    
    # Initialize Database (Create tables)
    init_db()
    
    # Build Application
    if not settings.TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set!")

    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", list_handler))
    application.add_handler(CommandHandler("add", add_item_handler))
    application.add_handler(CommandHandler("list", list_handler))
    application.add_handler(CommandHandler("clear", clear_handler))
    application.add_handler(CommandHandler("suggest", suggestions_handler))
    
    logger.info("Bot is ready to poll.")
    # Start Polling
    application.run_polling()

if __name__ == "__main__":
    main()
