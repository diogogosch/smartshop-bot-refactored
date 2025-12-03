"""Settings handler for user preferences."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User

logger = logging.getLogger(__name__)

# Valid currency codes
VALID_CURRENCIES = ["USD", "BRL", "EUR", "GBP", "ARS", "MXN", "COP"]
# Valid language codes
VALID_LANGUAGES = ["en", "pt", "es", "fr", "de"]


async def set_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /currency command - Set preferred currency."""
    user_id = update.effective_user.id
    
    try:
        if not context.args:
            await update.message.reply_text(
                f"❌ Usage: /currency <code>\n\n"
                f"Valid currencies: {', '.join(VALID_CURRENCIES)}"
            )
            return
        
        currency = context.args[0].upper()
        
        if currency not in VALID_CURRENCIES:
            await update.message.reply_text(
                f"❌ Invalid currency '{currency}'.\n\n"
                f"Valid options: {', '.join(VALID_CURRENCIES)}"
            )
            return
        
        # Save to database
        try:
            async with AsyncSessionLocal() as session:
                stmt = select(User).where(User.user_id == user_id)
                user = await session.scalar(stmt)
                
                if user:
                    user.preferred_currency = currency
                    await session.commit()
                    await update.message.reply_text(
                        f"✅ Currency set to {currency}"
                    )
                    logger.info(f"User {user_id} set currency to {currency}")
                else:
                    await update.message.reply_text(
                        "❌ User profile not found. Please use /start first."
                    )
        except Exception as db_error:
            logger.error(f"Database error setting currency: {db_error}")
            await update.message.reply_text(
                "❌ Error saving currency preference. Please try again."
            )
    except Exception as e:
        logger.error(f"Error in set_currency: {e}")
        await update.message.reply_text(
            "❌ Error processing currency setting. Please try again."
        )


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /language command - Set preferred language."""
    user_id = update.effective_user.id
    
    try:
        if not context.args:
            await update.message.reply_text(
                f"❌ Usage: /language <code>\n\n"
                f"Valid languages: {', '.join(VALID_LANGUAGES)}\n\n"
                f"en - English\npt - Portuguese\nes - Spanish\n"
                f"fr - French\nde - German"
            )
            return
        
        lang_code = context.args[0].lower()
        
        if lang_code not in VALID_LANGUAGES:
            await update.message.reply_text(
                f"❌ Invalid language '{lang_code}'.\n\n"
                f"Valid options: {', '.join(VALID_LANGUAGES)}"
            )
            return
        
        # Save to database
        try:
            async with AsyncSessionLocal() as session:
                stmt = select(User).where(User.user_id == user_id)
                user = await session.scalar(stmt)
                
                if user:
                    user.preferred_language = lang_code
                    await session.commit()
                    await update.message.reply_text(
                        f"✅ Language set to {lang_code.upper()}"
                    )
                    logger.info(f"User {user_id} set language to {lang_code}")
                else:
                    await update.message.reply_text(
                        "❌ User profile not found. Please use /start first."
                    )
        except Exception as db_error:
            logger.error(f"Database error setting language: {db_error}")
            await update.message.reply_text(
                "❌ Error saving language preference. Please try again."
            )
    except Exception as e:
        logger.error(f"Error in set_language: {e}")
        await update.message.reply_text(
            "❌ Error processing language setting. Please try again."
        )


async def manage_stores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stores command - Manage favorite stores."""
    user_id = update.effective_user.id
    
    try:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.user_id == user_id)
            user = await session.scalar(stmt)
            
            if user:
                # TODO: Implement store management logic when Store model is ready
                stores_text = "\n".join([
                    "1. Carrefour - Av. Paulista",
                    "2. Pao de Acucar - Centro",
                    "3. Dia - Vila Mariana"
                ])
                
                await update.message.reply_text(
                    f"🏪 <b>Your Favorite Stores:</b>\n\n{stores_text}\n\n"
                    f"<b>Commands:</b>\n"
                    f"/addstore <name> - Add a store\n"
                    f"/removestore <id> - Remove a store",
                    parse_mode="HTML"
                )
                logger.info(f"User {user_id} viewed favorite stores")
            else:
                await update.message.reply_text(
                    "❌ User profile not found. Please use /start first."
                )
    except Exception as e:
        logger.error(f"Error in manage_stores: {e}")
        await update.message.reply_text(
            "❌ Error retrieving stores. Please try again."
        )


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command - Show current settings."""
    user_id = update.effective_user.id
    
    try:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.user_id == user_id)
            user = await session.scalar(stmt)
            
            if user:
                currency = user.preferred_currency or "BRL"
                language = user.preferred_language or "en"
                notifications = "Enabled" if getattr(user, "notifications_enabled", True) else "Disabled"
                
                settings_text = (
                    f"⚙️ <b>Your Settings:</b>\n\n"
                    f"💵 <b>Currency:</b> {currency}\n"
                    f"🗣️ <b>Language:</b> {language.upper()}\n"
                    f"🔔 <b>Notifications:</b> {notifications}\n"
                    f"📊 <b>Total Items:</b> {user.item_count or 0}\n"
                    f"🧾 <b>Receipts Processed:</b> {user.receipt_count or 0}\n\n"
                    f"<b>Change Settings:</b>\n"
                    f"/currency <code> - Change currency\n"
                    f"/language <code> - Change language"
                )
                
                await update.message.reply_text(settings_text, parse_mode="HTML")
                logger.info(f"User {user_id} viewed settings")
            else:
                await update.message.reply_text(
                    "❌ User profile not found. Please use /start first."
                )
    except Exception as e:
        logger.error(f"Error in show_settings: {e}")
        await update.message.reply_text(
            "❌ Error retrieving settings. Please try again."
        )
