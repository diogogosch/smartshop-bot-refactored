"""Base handler for Telegram bot."""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - Welcome message."""
    try:
        user = update.effective_user
        welcome_text = (
            f"👋 Welcome to SmartShopBot, {user.first_name}!\n\n"
            "📝 **Available Commands:**\n"
            "/add <item> - Add item to shopping list\n"
            "/list - View your shopping list\n"
            "/remove <number> - Remove item by number\n"
            "/clear - Clear entire list\n"
            "/suggestions - Get AI suggestions\n"
            "/receipt - Process receipt photo\n"
            "/stats - View spending stats\n"
            "/currency - Set preferred currency\n"
            "/language - Set language\n"
            "/help - Show this help message\n\n"
            "🚀 Type /add to get started!"
        )
        await update.message.reply_text(welcome_text, parse_mode="Markdown")
        logger.info(f"User {user.id} started bot")
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text(
            "❌ An error occurred. Please try again."
        )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command - Show help message."""
    try:
        help_text = (
            "📚 **SmartShopBot Help**\n\n"
            "**Shopping List Commands:**\n"
            "`/add <item>` - Add item\n"
            "  Example: /add Milk\n"
            "`/list` - View all items\n"
            "`/remove <n>` - Remove item\n"
            "  Example: /remove 1\n"
            "`/clear` - Clear list\n\n"
            "**AI & Features:**\n"
            "`/suggestions` - Get AI suggestions\n"
            "`/receipt` - Upload receipt photo\n"
            "`/stats` - Spending statistics\n\n"
            "**Settings:**\n"
            "`/currency <code>` - Set currency (USD, BRL, EUR)\n"
            "`/language <code>` - Set language (en, pt, es)\n\n"
            "❓ Need more help? Check documentation on GitHub."
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
        logger.info(f"User {update.effective_user.id} requested help")
    except Exception as e:
        logger.error(f"Error in help_handler: {e}")
        await update.message.reply_text(
            "❌ Error displaying help. Please try again."
        )
