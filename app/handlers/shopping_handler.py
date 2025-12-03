"""Shopping list handler for managing items."""
import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.shopping import ShoppingItem
from app.models.user import User
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)


async def ensure_user(user_id: int, username: str, db=None) -> User:
    """Ensure user exists in database."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            user = User(id=user_id, username=username)
            session.add(user)
            await session.commit()
        return user


async def add_item_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /add command - Add item to shopping list."""
    try:
        if not context.args:
            await update.message.reply_text(
                "📝 Usage: /add <item name> [quantity]\n"
                "Example: /add Milk 2"
            )
            return

        item_text = " ".join(context.args)
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"

        async with AsyncSessionLocal() as db:
            try:
                # Ensure user exists
                user = await ensure_user(user_id, username)
                
                # Create new shopping item
                new_item = ShoppingItem(
                    user_id=user_id,
                    name=item_text
                )
                db.add(new_item)
                await db.commit()
                
                await update.message.reply_text(
                    f"✅ Added: {item_text}"
                )
                logger.info(f"User {user_id} added item: {item_text}")
                
            except Exception as e:
                await db.rollback()
                logger.error(f"Error adding item for user {user_id}: {e}")
                await update.message.reply_text(
                    "❌ Error adding item. Please try again."
                )
    except Exception as e:
        logger.error(f"Unexpected error in add_item_handler: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred."
        )


async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /list command - Display shopping list."""
    try:
        user_id = update.effective_user.id
        
        async with AsyncSessionLocal() as db:
            try:
                # Get all items for this user
                result = await db.execute(
                    select(ShoppingItem).where(ShoppingItem.user_id == user_id)
                )
                items = result.scalars().all()
                
                if not items:
                    await update.message.reply_text(
                        "📋 Your shopping list is empty.\n"
                        "Use /add to add items."
                    )
                    return
                
                msg = "📋 **Your Shopping List:**\n\n"
                for i, item in enumerate(items, 1):
                    msg += f"{i}. {item.name}\n"
                
                await update.message.reply_text(msg, parse_mode="Markdown")
                logger.info(f"User {user_id} viewed list with {len(items)} items")
                
            except Exception as e:
                logger.error(f"Error retrieving list for user {user_id}: {e}")
                await update.message.reply_text(
                    "❌ Error retrieving list. Please try again."
                )
    except Exception as e:
        logger.error(f"Unexpected error in list_handler: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred."
        )


async def remove_item_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remove command - Remove item from shopping list."""
    try:
        if not context.args:
            await update.message.reply_text(
                "📝 Usage: /remove <item number>\n"
                "First use /list to see item numbers."
            )
            return
        
        try:
            item_index = int(context.args[0]) - 1
        except ValueError:
            await update.message.reply_text(
                "❌ Please provide a valid item number."
            )
            return
        
        user_id = update.effective_user.id
        
        async with AsyncSessionLocal() as db:
            try:
                # Get all items and remove by index
                result = await db.execute(
                    select(ShoppingItem).where(ShoppingItem.user_id == user_id)
                )
                items = result.scalars().all()
                
                if item_index < 0 or item_index >= len(items):
                    await update.message.reply_text(
                        "❌ Invalid item number."
                    )
                    return
                
                item_to_remove = items[item_index]
                await db.delete(item_to_remove)
                await db.commit()
                
                await update.message.reply_text(
                    f"✅ Removed: {item_to_remove.name}"
                )
                logger.info(f"User {user_id} removed item: {item_to_remove.name}")
                
            except Exception as e:
                await db.rollback()
                logger.error(f"Error removing item for user {user_id}: {e}")
                await update.message.reply_text(
                    "❌ Error removing item. Please try again."
                )
    except Exception as e:
        logger.error(f"Unexpected error in remove_item_handler: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred."
        )


async def clear_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command - Clear entire shopping list."""
    try:
        user_id = update.effective_user.id
        
        async with AsyncSessionLocal() as db:
            try:
                # Delete all items for this user
                result = await db.execute(
                    select(ShoppingItem).where(ShoppingItem.user_id == user_id)
                )
                items = result.scalars().all()
                
                if not items:
                    await update.message.reply_text(
                        "📋 Your shopping list is already empty."
                    )
                    return
                
                count = len(items)
                for item in items:
                    await db.delete(item)
                await db.commit()
                
                await update.message.reply_text(
                    f"✅ Cleared {count} items from your list."
                )
                logger.info(f"User {user_id} cleared {count} items")
                
            except Exception as e:
                await db.rollback()
                logger.error(f"Error clearing list for user {user_id}: {e}")
                await update.message.reply_text(
                    "❌ Error clearing list. Please try again."
                )
    except Exception as e:
        logger.error(f"Unexpected error in clear_handler: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred."
        )


async def suggestions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /suggestions command - Get AI suggestions."""
    try:
        user_id = update.effective_user.id
        
        async with AsyncSessionLocal() as db:
            try:
                # Get all items for this user
                result = await db.execute(
                    select(ShoppingItem).where(ShoppingItem.user_id == user_id)
                )
                items = result.scalars().all()
                
                if not items:
                    await update.message.reply_text(
                        "📋 Your shopping list is empty.\n"
                        "Add items first to get suggestions."
                    )
                    return
                
                current_names = [i.name for i in items]
                
                if not ai_service.client:
                    await update.message.reply_text(
                        "⚠️ AI suggestions are currently disabled."
                    )
                    return
                
                await update.message.reply_text(
                    "🤖 Thinking of suggestions..."
                )
                
                suggestions = await ai_service.get_suggestions(current_names)
                
                msg = "🤖 **AI Suggestions:**\n\n"
                for s in suggestions:
                    msg += f"• {s}\n"
                
                await update.message.reply_text(
                    msg,
                    parse_mode="Markdown"
                )
                logger.info(f"User {user_id} got AI suggestions")
                
            except Exception as e:
                logger.error(f"Error getting suggestions for user {user_id}: {e}")
                await update.message.reply_text(
                    "❌ Error getting suggestions. Please try again."
                )
    except Exception as e:
        logger.error(f"Unexpected error in suggestions_handler: {e}")
        await update.message.reply_text(
            "❌ An unexpected error occurred."
        )
