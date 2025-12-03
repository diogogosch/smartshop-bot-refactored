import logging
import asyncio
from aiohttp import web
from telegram.ext import ApplicationBuilder, Application

from app.config.settings import settings
# Import your handlers here:
# from app.handlers.shopping import shopping_router

# Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.LOG_LEVEL
)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_http_server():
    """Starts a simple background HTTP server for Docker Healthchecks"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.HOST, settings.PORT)
    await site.start()
    logger.info(f"Health check server started on {settings.HOST}:{settings.PORT}")

async def post_init(application: Application):
    """Post initialization hook"""
    await start_http_server()
    logger.info("Bot is fully initialized and running.")

def main():
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

    # --- REGISTER HANDLERS HERE ---
    # application.add_handler(CommandHandler("start", start_handler))
    
    # Run
    application.run_polling()

if __name__ == '__main__':
    main()
