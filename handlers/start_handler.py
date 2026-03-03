# handlers/start_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menu_keyboard import categories_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    full_name = user.full_name

    await update.message.reply_text(
    f"🍽️ Welcome to *Delicious Restaurant*, {full_name}! 😋\n\n"
    "Please browse our menu and choose a category to get started:",
    reply_markup=categories_keyboard(),
    parse_mode="Markdown"
)