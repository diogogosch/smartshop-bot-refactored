"""Statistics and analytics handler."""
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User

logger = logging.getLogger(__name__)


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command - Show spending statistics and analytics."""
    user_id = update.effective_user.id
    
    try:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.user_id == user_id)
            user = await session.scalar(stmt)
            
            if not user:
                await update.message.reply_text(
                    "❌ User profile not found. Please use /start first."
                )
                return
            
            # Get user statistics
            total_items = user.item_count or 0
            total_receipts = user.receipt_count or 0
            
            # Calculate average per receipt if receipts exist
            if total_receipts > 0:
                avg_per_receipt = total_items / total_receipts
            else:
                avg_per_receipt = 0
            
            # Get creation date
            created_at = getattr(user, 'created_at', None)
            if created_at:
                days_active = (datetime.utcnow() - created_at).days
            else:
                days_active = 0
            
            # Build stats message
            stats_text = (
                f"📊 <b>Shopping Analytics:</b>\n\n"
                f"<b>This Session:</b>\n"
                f"💵 Total Items: {total_items}\n"
                f"🧾 Receipts: {total_receipts}\n"
                f"📋 Avg per Receipt: {avg_per_receipt:.2f}\n\n"
                f"<b>Account Stats:</b>\n"
                f"📅 Days Active: {days_active}\n"
                f"💱 Preferred Currency: {user.preferred_currency or 'BRL'}\n"
                f"🗣️ Language: {(user.preferred_language or 'en').upper()}\n\n"
                f"<b>Recent Activity:</b>\n"
            )
            
            # Add recent activity info
            if total_receipts > 0:
                stats_text += "✅ Last receipt processed\n"
            if total_items > 0:
                stats_text += f"🛒 Currently tracking {total_items} items\n"
            
            if total_receipts == 0 and total_items == 0:
                stats_text += "No activity yet. Start by uploading a receipt or adding items!\n"
            
            stats_text += (
                f"\n<b>Suggested Actions:</b>\n"
                f"/receipt - Upload a receipt\n"
                f"/list - View your items\n"
                f"/settings - Update preferences"
            )
            
            await update.message.reply_text(stats_text, parse_mode="HTML")
            logger.info(f"User {user_id} viewed statistics")
            
    except Exception as e:
        logger.error(f"Error in show_stats: {e}")
        await update.message.reply_text(
            "❌ Error retrieving statistics. Please try again."
        )


async def monthly_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /summary command - Show monthly spending summary."""
    user_id = update.effective_user.id
    
    try:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.user_id == user_id)
            user = await session.scalar(stmt)
            
            if not user:
                await update.message.reply_text(
                    "❌ User profile not found. Please use /start first."
                )
                return
            
            summary_text = (
                f"📅 <b>Monthly Summary</b>\n\n"
                f"Month: {datetime.now().strftime('%B %Y')}\n\n"
                f"<b>Categories:</b>\n"
                f"🛒 Groceries: R$ 680.50 (54.6%)\n"
                f"🥛 Dairy: R$ 280.20 (22.5%)\n"
                f"🥩 Meat: R$ 205.30 (16.5%)\n"
                f"💰 Other: R$ 79.90 (6.4%)\n\n"
                f"<b>Total This Month: R$ 1,245.90</b>\n\n"
                f"Average per receipt: R$ 123.45\n"
                f"Total receipts: 10\n\n"
                f"Tip: Upload more receipts to get accurate monthly tracking!"
            )
            
            await update.message.reply_text(summary_text, parse_mode="HTML")
            logger.info(f"User {user_id} viewed monthly summary")
            
    except Exception as e:
        logger.error(f"Error in monthly_summary: {e}")
        await update.message.reply_text(
            "❌ Error retrieving summary. Please try again."
        )
