from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def item_keyboard(item_id):
    buttons = [
        [InlineKeyboardButton("Add to Cart", callback_data=f"add_{item_id}")]
    ]
    return InlineKeyboardMarkup(buttons)

def cart_item_keyboard(cart_id):
    buttons = [
        [InlineKeyboardButton("Remove", callback_data=f"remove_{cart_id}")]
    ]
    return InlineKeyboardMarkup(buttons)