"""Receipt processing handler."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.services.ocr_service import ocr_service
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User

logger = logging.getLogger(__name__)


async def process_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /receipt command or photo upload - Process receipt with OCR."""
    user_id = update.effective_user.id
    
    try:
        if update.message.photo:
            # Notify user that processing has started
            await update.message.reply_text("🔄 Processing receipt...")
            
            # Download the photo
            photo_file = await update.message.photo[-1].get_file()
            image_data = await photo_file.download_as_bytearray()
            
            # Process with OCR service
            try:
                result = await ocr_service.process_receipt(bytes(image_data))
                
                if result and result.get("success") and result.get("items"):
                    # Format items for display
                    items_text = "\n".join([
                        f"• {item.get('name', 'Unknown')}: R${item.get('price', 0):.2f}" 
                        for item in result["items"]
                    ])
                    total = sum(item.get('price', 0) for item in result["items"])
                    
                    # Save to database
                    try:
                        async with AsyncSessionLocal() as session:
                            stmt = select(User).where(User.user_id == user_id)
                            user = await session.scalar(stmt)
                            
                            if user:
                                # Update user's receipt count
                                user.receipt_count = (user.receipt_count or 0) + 1
                                await session.commit()
                    except Exception as db_error:
                        logger.warning(f"Could not update user stats: {db_error}")
                    
                    # Send processed receipt
                    await update.message.reply_text(
                        f"✅ Receipt processed!\n\n"
                        f"<b>Extracted items:</b>\n{items_text}\n\n"
                        f"<b>Total: R${total:.2f}</b>",
                        parse_mode="HTML"
                    )
                    logger.info(f"User {user_id} processed receipt with OCR")
                else:
                    # OCR couldn't extract items
                    await update.message.reply_text(
                        "❌ Could not extract items from receipt. "
                        "The image may be unclear. Please try again."
                    )
                    logger.warning(f"User {user_id} - OCR extraction failed")
            except Exception as ocr_error:
                logger.error(f"OCR service error: {ocr_error}")
                await update.message.reply_text(
                    "❌ Error processing receipt with OCR. Please try again."
                )
        else:
            # No photo attached
            await update.message.reply_text(
                "📷 Please send a photo of your receipt to process it.\n\n"
                "Supported formats: JPG, PNG"
            )
    except Exception as e:
        logger.error(f"Error in process_receipt: {e}")
        await update.message.reply_text(
            "❌ Error processing receipt. Please try again."
        )
