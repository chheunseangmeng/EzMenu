from services.cart_service import (
    add_to_temp_cart,
    get_temp_cart,
    remove_from_temp_cart,
    clear_temp_cart
)
from services.menu_service import get_menu_items
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.menu_handler import categories_keyboard
from handlers.checkout_handler import checkout_handler

# Add item
async def add_item(update, context, item_id):
    telegram_id = update.callback_query.from_user.id
    items = get_menu_items()
    item = next((i for i in items if i["id"] == item_id), None)

    if item:
        add_to_temp_cart(telegram_id, item)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("View Cart 🛒", callback_data="view_cart")]
        ])
        await update.callback_query.message.reply_text(
            "✅ Item added to cart!",
            reply_markup=keyboard
        )

# View cart
async def view_cart_handler(update, context):
    telegram_id = update.callback_query.from_user.id
    cart_items = get_temp_cart(telegram_id)

    if not cart_items:
        await update.callback_query.message.reply_text("Your cart is empty! 😢")
        return

    total = sum(i["price"] * i["quantity"] for i in cart_items)
    text = "🛒 *Your Cart:*\n\n"

    remove_buttons = []
    for item in cart_items:
        text += f"{item['name']} x{item['quantity']} — ${item['price']*item['quantity']:.2f}\n"
        remove_buttons.append(
            InlineKeyboardButton(
                f"❌ Remove {item['name']}",
                callback_data=f"remove_{item['id']}"
            )
        )


    keyboard = []
    
    
    for i in range(0, len(remove_buttons), 2):
        if i+1 < len(remove_buttons):
            keyboard.append([remove_buttons[i], remove_buttons[i+1]])
        else:
            keyboard.append([remove_buttons[i]])
    
    keyboard.append([
        InlineKeyboardButton("💳 Checkout", callback_data="checkout"),
        InlineKeyboardButton("🔄 Continue Choosing", callback_data="continue")
    ])

    await update.callback_query.message.reply_text(
        text + f"\n*Total: ${total:.2f}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def remove_item(update, context, item_id):
    telegram_id = update.callback_query.from_user.id
    remove_from_temp_cart(telegram_id, item_id)
    await view_cart_handler(update, context)


async def continue_choosing(update, context):
    await update.callback_query.message.reply_text(
        "📂 Choose a category:",
        reply_markup=categories_keyboard()
    )