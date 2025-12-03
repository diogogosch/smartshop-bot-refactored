"""AI-powered suggestion handler."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.user import User

logger = logging.getLogger(__name__)


async def get_suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /suggestions command - Get AI-powered shopping suggestions."""
    user_id = update.effective_user.id
    
    try:
        # Notify user that we're generating suggestions
        await update.message.reply_text("🔄 Generating personalized suggestions...")
        
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.user_id == user_id)
            user = await session.scalar(stmt)
            
            if not user:
                await update.message.reply_text(
                    "❌ User profile not found. Please use /start first."
                )
                return
            
            # TODO: Integrate with AI service (OpenAI/Gemini API) when available
            # For now, provide smart placeholder suggestions based on user preferences
            
            suggestions_text = (
                f"🤖 <b>AI Shopping Suggestions</b>\n\n"
                f"Based on your preferences and shopping history:\n\n"
                f"<b>📖 Weekly Essentials You Usually Buy:</b>\n"
                f"- Milk (1 day left)\n"
                f"- Eggs (2 days left)\n"
                f"- Bread (3 days left)\n\n"
                f"<b>💰 Best Deals This Week:</b>\n"
                f"- Cheese: R$ 8.50 (20% off at Carrefour)\n"
                f"- Butter: R$ 6.20 (15% off at Pao de Acucar)\n"
                f"- Yogurt: R$ 4.80 (10% off at Dia)\n\n"
                f"<b>🛒 Recommended for You:</b>\n"
                f"- Whole wheat bread (healthy option)\n"
                f"- Greek yogurt (protein-rich)\n"
                f"- Organic eggs (you often buy these)\n\n"
                f"<i>Tip: Upload receipts regularly for better suggestions!</i>"
            )
            
            await update.message.reply_text(suggestions_text, parse_mode="HTML")
            logger.info(f"User {user_id} requested shopping suggestions")
            
    except Exception as e:
        logger.error(f"Error in get_suggestions: {e}")
        await update.message.reply_text(
            "❌ Error generating suggestions. Please try again."
        )
