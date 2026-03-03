# This code is group photo---------------------------------------------------------
from keyboards.menu_keyboard import categories_keyboard
from services.menu_service import get_menu_items
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ParseMode

async def show_category(update, context, category):
    items = get_menu_items(category)
    
    if not items:
        await update.callback_query.message.reply_text("No items found! Please choose another category.")
        await update.callback_query.message.reply_text(
            "📂 Choose a category:",
            reply_markup=categories_keyboard()
        )
        return

    # Send items in groups of 2
    for i in range(0, len(items), 2):
        pair = items[i:i+2]
        
        # Create media group with 2 photos together
        media_group = []
        for item in pair:
            khr_price = f"{item['price_khr']:,}".replace(',', ',')
            caption = f"*{item['name']}*\n"
            caption += f"_{item['description']}_\n\n"
            caption += f"🇺🇸 ${item['price']:.2f}  |  🇰🇭 {khr_price}៛"
            
            media_group.append(
                InputMediaPhoto(
                    media=open(item['image_url'], 'rb'),
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            )
        
        # MESSAGE 1: Send both photos together
        await update.callback_query.message.reply_media_group(media_group)
    
        invisible_space = "\u2003" * 1  
        
        # Create buttons with invisible spaces for width
        buttons = []
        for item in pair:
            button_text = f"{invisible_space}🛒 Add {item['name']}{invisible_space}"
            
            buttons.append(
                InlineKeyboardButton(button_text, callback_data=f"add_{item['id']}")
            )
        
        # MESSAGE 2: Send both buttons together
        keyboard = InlineKeyboardMarkup([buttons])
        await update.callback_query.message.reply_text(
            "select Item",  # Minimal text
            reply_markup=keyboard
        )
    
    # Show categories again
    await update.callback_query.message.reply_text(
        "📂 *Choose another category* or view your cart:",
        reply_markup=categories_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )
    
    
    
# This code is deliver one by one as separateed

# from keyboards.menu_keyboard import categories_keyboard
# from services.menu_service import get_menu_items
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.constants import ParseMode

# async def show_category(update, context, category):
#     items = get_menu_items(category)
    
#     if not items:
#         await update.callback_query.message.reply_text("No items found! Please choose another category.")
#         await update.callback_query.message.reply_text(
#             "📂 Choose a category:",
#             reply_markup=categories_keyboard()
#         )
#         return

#     # Send each item individually
#     for item in items:
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton("🛒 Add to Cart", callback_data=f"add_{item['id']}")]
#         ])
        
#         # Format KHR price with commas
#         khr_price = f"{item['price_khr']:,}".replace(',', ',')
        
#         # Caption with both USD and KHR
#         caption = f"*{item['name']}*\n"
#         caption += f"_{item['description']}_\n\n"
#         caption += f" *USD:* ${item['price']:.2f}\n"
#         caption += f" *KHR:* {khr_price}៛"
        
#         await update.callback_query.message.reply_photo(
#             photo=open(item['image_url'], 'rb'),
#             caption=caption,
#             reply_markup=keyboard,
#             parse_mode=ParseMode.MARKDOWN
#         )
    
#     # AFTER all items are sent, show categories again for more choosing
#     await update.callback_query.message.reply_text(
#         "📂 *Choose another category* or view your cart:",
#         reply_markup=categories_keyboard(),
#         parse_mode=ParseMode.MARKDOWN
#     )