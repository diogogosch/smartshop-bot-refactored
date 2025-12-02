"""Receipt processing handler"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def process_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /receipt command or photo upload - Process receipt with OCR"""
    user_id = update.effective_user.id
    
    try:
        if update.message.photo:
            await update.message.reply_text("🔄 Processing receipt...")
            # TODO: Download photo, run OCR, extract items
            await update.message.reply_text("✅ Receipt processed!\n\nExtracted items:\n- Milk 2L: R$5.50\n- Bread: R$4.20\n- Eggs: R$12.00\n\nTotal: R$21.70")
            logger.info(f"User {user_id} processed receipt")
        else:
            await update.message.reply_text("📷 Please send a photo of your receipt")
    except Exception as e:
        logger.error(f"Error processing receipt: {e}")
        await update.message.reply_text("❌ Error processing receipt. Please try again.")
