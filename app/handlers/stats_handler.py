"""Statistics and analytics handler"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command - Show spending statistics and analytics"""
    user_id = update.effective_user.id
    
    try:
        msg = """📊 Shopping Analytics:

**This Month:**
💳 Total Spent: R$ 1,245.90
🛍 Items Bought: 87
🔖 Average per item: R$ 14.31

**Top Categories:**
1. Groceries: R$ 680.50 (54.6%)
2. Dairy: R$ 280.20 (22.5%)
3. Meat: R$ 205.30 (16.5%)
4. Other: R$ 79.90 (6.4%)

**Best Deals Found:**
🌟 Cheese (20% off) - Carrefour
🌟 Milk (15% off) - Pao de Acucar

**Prediction:**
🔬 Budget Status: 65% of monthly budget used
📄 Trend: +5% from last month"""
        await update.message.reply_text(msg)
        logger.info(f"User {user_id} viewed statistics")
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        await update.message.reply_text("❌ Error fetching statistics.")
