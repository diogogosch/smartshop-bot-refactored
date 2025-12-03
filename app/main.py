import logging
import asyncio
from aiohttp import web
from telegram.ext import ApplicationBuilder, Application, CommandHandler
from app.core.database import engine, Base
from app import models  # Register all models for DB creation

from app.config.settings import settings
from app.handlers.shopping_handler import (
    add_item_handler,
    list_handler,
    remove_item_handler,
    clear_handler,
    suggestions_handler,
)
from app.handlers.receipt_handler import receipt_handler
from app.handlers.settings_handler import set_currency, set_language
from app.handlers.stats_handler import stats_handler
from app.handlers.base import start_handler, help_handler

# Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.LOG_LEVEL
)
logger = logging.getLogger(__name__)


async def health_check(request):
    """Health check endpoint for Docker."""
    return web.Response(text="OK", status=200)


async def start_http_server():
    """Starts a simple background HTTP server for Docker Healthchecks."""
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.HOST, settings.PORT)
    await site.start()
    logger.info(f"Health check server started on {settings.HOST}:{settings.PORT}")


async def post_init(application: Application):
    """Post initialization hook."""
    await start_http_server()
        # Create all database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")
    logger.info("Bot is fully initialized and running.")


def main():
    """Main bot entry point."""
    if not settings.TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN is missing!")
        return

    logger.info("Starting SmartShopBot...")

    # Build Application
    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    # --- REGISTER COMMAND HANDLERS ---
    logger.info("Registering command handlers...")
    
    # Basic commands
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    
    # Shopping list commands
    application.add_handler(CommandHandler("add", add_item_handler))
    application.add_handler(CommandHandler("remove", remove_item_handler))
    application.add_handler(CommandHandler("list", list_handler))
    application.add_handler(CommandHandler("clear", clear_handler))
    
    # AI suggestions
    application.add_handler(CommandHandler("suggestions", suggestions_handler))
    
    # Receipt processing
    application.add_handler(CommandHandler("receipt", receipt_handler))
    
    # Statistics
    application.add_handler(CommandHandler("stats", stats_handler))
    
    # Settings
    application.add_handler(CommandHandler("currency", set_currency))
    application.add_handler(CommandHandler("language", set_language))
    
    logger.info(f"Registered 11 command handlers")
    
    # Run
    logger.info("Bot polling started...")
    application.run_polling()


if __name__ == '__main__':
    main()
