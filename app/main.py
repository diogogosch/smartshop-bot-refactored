"""SmartShopBot - Main Application Entry Point"""
import sys
import os
import logging
import threading
import schedule
import time
from aiohttp import web

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartShopBot:
    """Main bot application class"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = None
        
    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command handler"""
        welcome_msg = f"""
🛒 Welcome to SmartShopBot!

I'll help you manage your shopping lists with AI-powered suggestions.

퉰b Commands:
✅ /add <item> - Add item to list
✅ /list - View your list
✅ /remove <item> - Remove item
✅ /clear - Clear entire list
✅ /suggestions - Get AI recommendations
✅ /receipt - Process receipt photo
✅ /stats - View spending analytics
✅ /settings - Configure preferences
✅ /help - Full command list
        """
        await update.message.reply_text(welcome_msg)
        logger.info(f"User {update.effective_user.id} started bot")
    
    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command handler"""
        help_msg = """
👋 Available Commands:

**Shopping List Management:**
/add <item> <qty> - Add item (e.g., /add milk 2L)
/list - Show all items
/remove <item> - Remove item from list
/clear - Clear entire list

**AI & Suggestions:**
/suggestions - Get personalized suggestions
/receipt - Upload receipt for processing

**Settings:**
/currency <code> - Set currency (USD, BRL, EUR)
/language <code> - Set language (en, pt, es)
/settings - View current settings

**Analytics:**
/stats - View spending statistics
/stores - Manage favorite stores
        """
        await update.message.reply_text(help_msg)
    
    async def add_item_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /add command"""
        if not context.args:
            await update.message.reply_text("❌ Usage: /add <item> [quantity]")
            return
        
        item = ' '.join(context.args)
        await update.message.reply_text(f"✅ Added: {item}")
        logger.info(f"User {update.effective_user.id} added: {item}")
    
    async def list_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /list command"""
        msg = """📝 Your Shopping List:

1. Milk 2L
2. Bread
3. Eggs (12)

Total Items: 3
        """
        await update.message.reply_text(msg)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Exception: {context.error}")
        if update:
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    async def health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint"""
        return web.Response(text="OK", status=200)
    
    def run_health_server(self) -> None:
        """Run health check server on port 8080"""
        app = web.Application()
        app.router.add_get('/health', self.health_check)
        runner = web.AppRunner(app)
        
        # Run in event loop
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        loop.run_until_complete(site.start())
        logger.info("Health check server running on :8080")
    
    def setup_handlers(self) -> None:
        """Setup bot command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_handler))
        self.application.add_handler(CommandHandler("help", self.help_handler))
        self.application.add_handler(CommandHandler("add", self.add_item_handler))
        self.application.add_handler(CommandHandler("list", self.list_handler))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start(self) -> None:
        """Start the bot"""
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Start health check server in separate thread
        health_thread = threading.Thread(target=self.run_health_server, daemon=True)
        health_thread.start()
        
        # Start polling
        logger.info("Starting bot polling...")
        await self.application.run_polling()


def main() -> None:
    """Main entry point"""
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error("TELEGRAM_TOKEN not set")
        sys.exit(1)
    
    bot = SmartShopBot(token)
    
    import asyncio
    asyncio.run(bot.start())


if __name__ == "__main__":
    main()
