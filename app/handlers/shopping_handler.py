from telegram import Update
from telegram.ext import ContextTypes
from app.core.database import SessionLocal
from app.models.shopping import User, ShoppingItem
from app.services.ai_service import ai_service

async def ensure_user(user_id: int, username: str, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=username)
        db.add(user)
        db.commit()
    return user

async def add_item_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /add <item name>")
        return

    item_text = " ".join(context.args)
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    with SessionLocal() as db:
        await ensure_user(user_id, username, db)
        new_item = ShoppingItem(user_id=user_id, name=item_text)
        db.add(new_item)
        db.commit()
    
    await update.message.reply_text(f"✅ Added: {item_text}")

async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    with SessionLocal() as db:
        items = db.query(ShoppingItem).filter(ShoppingItem.user_id == user_id).all()
        
    if not items:
        await update.message.reply_text("📝 Your list is empty.")
        return

    msg = "📝 **Your Shopping List**:\n"
    for i, item in enumerate(items, 1):
        msg += f"{i}. {item.name}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def clear_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    with SessionLocal() as db:
        db.query(ShoppingItem).filter(ShoppingItem.user_id == user_id).delete()
        db.commit()
    await update.message.reply_text("🗑 List cleared.")

async def suggestions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    with SessionLocal() as db:
        items = db.query(ShoppingItem).filter(ShoppingItem.user_id == user_id).all()
        current_names = [i.name for i in items]
    
    if not current_names:
        await update.message.reply_text("⚠️ Add items to your list first to get suggestions!")
        return

    await update.message.reply_text("🤖 Thinking of suggestions...")
    suggestions = await ai_service.get_suggestions(current_names)
    
    msg = "💡 **AI Suggestions:**\n" + "\n".join([f"• {s}" for s in suggestions])
    await update.message.reply_text(msg, parse_mode="Markdown")
