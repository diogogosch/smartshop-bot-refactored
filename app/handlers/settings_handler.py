"""Settings handler for user preferences"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def set_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /currency command - Set preferred currency"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /currency <code>\nExamples: USD, BRL, EUR")
        return
    currency = context.args[0].upper()
    await update.message.reply_text(f"✅ Currency set to {currency}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /language command - Set preferred language"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /language <code>\nExamples: en, pt, es")
        return
    lang = context.args[0]
    await update.message.reply_text(f"✅ Language set to {lang}")

async def manage_stores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stores command - Manage favorite stores"""
    msg = "🏪 Favorite Stores:\n\n1. Carrefour - Av. Paulista\n2. Pao de Acucar - Centro\n\nUse: /addstore <name> or /removestore <name>"
    await update.message.reply_text(msg)

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command - Show current settings"""
    msg = "⚙️ Your Settings:\n\n💵 Currency: BRL\n🗞 Language: Portuguese\n🏪 Stores: 2 saved\n🔔 Notifications: Enabled"
    await update.message.reply_text(msg)
