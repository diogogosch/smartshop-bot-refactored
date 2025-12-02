"""Receipt processing handler"""
from telegram import Update
from telegram.ext import ContextTypes
import logging
from app.services.ocr_service import ocr_service

logger = logging.getLogger(__name__)

async def process_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /receipt command or photo upload - Process receipt with OCR"""
    user_id = update.effective_user.id
    
    try:
        if update.message.photo:
            await update.message.reply_text("🔄 Processing receipt...")
photo_file = await update.message.photo[-1].get_file()
            image_data = await photo_file.download_as_bytearray()
            
            # Process with OCR
            result = await ocr_service.process_receipt(bytes(image_data))
            
            if result["success"] and result.get("items"):
                items_text = "\n".join([f"• {item['name']}: R${item['price']:.2f}" for item in result["items"]])
                total = sum(item['price'] for item in result["items"])
                
                await update.message.reply_text(
                    f"✅ Receipt processed!\n\n<b>Extracted items:</b>\n{items_text}\n\n<b>Total: R${total:.2f}</b>",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text("❌ Could not process receipt. Please try again.")
            
            logger.info(f"User {user_id} processed receipt")            await update.message.reply_text("✅ Receipt processed!\n\nExtracted items:\n- Milk 2L: R$5.50\n- Bread: R$4.20\n- Eggs: R$12.00\n\nTotal: R$21.70")
            logger.info(f"User {user_id} processed receipt")
        else:
            await update.message.reply_text("📷 Please send a photo of your receipt")
    except Exception as e:
        logger.error(f"Error processing receipt: {e}")
        await update.message.reply_text("❌ Error processing receipt. Please try again.")
