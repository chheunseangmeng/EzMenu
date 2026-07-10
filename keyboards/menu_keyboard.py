from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def categories_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🍕 Foods", callback_data="category_foods"),
            InlineKeyboardButton("🥤 Drinks", callback_data="category_drinks"),
            InlineKeyboardButton("🍰 Desserts", callback_data="category_desserts"),
            InlineKeyboardButton("All", callback_data="category_all")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)