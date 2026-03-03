from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers.start_handler import start
from handlers.menu_handler import show_category
from handlers.cart_handler import add_item, continue_choosing, remove_item, view_cart_handler
from handlers.checkout_handler import checkout_handler  
from config import TOKEN

# Handle all callback queries (button presses)
async def handle_callbacks(update, context):
    data = update.callback_query.data
    await update.callback_query.answer() 

    if data.startswith("category_"):
        category = data.split("_")[1]
        await show_category(update, context, category)
    elif data.startswith("add_"):
        item_id = int(data.split("_")[1])
        await add_item(update, context, item_id)
    elif data.startswith("remove_"):
        item_id = int(data.split("_")[1])
        await remove_item(update, context, item_id)
    elif data == "view_cart":
        await view_cart_handler(update, context)
    elif data == "checkout":
        await checkout_handler(update, context) 
    elif data == "continue":
        await continue_choosing(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callbacks))

print("Bot is running... 🚀")
app.run_polling()