from services.cart_service import get_temp_cart, clear_temp_cart
from services.receipt_service import generate_pdf_receipt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import get_connection

async def checkout_handler(update, context):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    telegram_id = user.id
    customer_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    cart_items = get_temp_cart(telegram_id)

    if not cart_items:
        await query.message.reply_text("Your cart is empty! 😢")
        return

    subtotal = 0

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # STEP 1: Get or create user to get user_id
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
        user_result = cursor.fetchone()

        if not user_result:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (telegram_id, first_name, last_name) VALUES (%s, %s, %s)",
                (telegram_id, user.first_name or '', user.last_name or '')
            )
            user_id = cursor.lastrowid
            print(f"Created new user with ID: {user_id}")
        else:
            user_id = user_result[0]
            print(f"Found existing user with ID: {user_id}")

        # STEP 2: Insert into carts table
        for item in cart_items:
            item_total = item["price"] * item["quantity"]
            cursor.execute(
                "INSERT INTO carts (user_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                (user_id, item["id"], item["quantity"], item_total)
            )
            subtotal += item_total
            print(f"Inserted item: {item['name']}, total: ${item_total}")

        conn.commit()
        print(f"Checkout completed for user {telegram_id}, total: ${subtotal}")

    except Exception as e:
        print(f"Error during checkout: {e}")
        conn.rollback()
        await query.message.reply_text("❌ Sorry, there was an error processing your order. Please try again.")
        return
    finally:
        cursor.close()
        conn.close()

    # STEP 3: Generate PDF receipt
    try:
        pdf_path = generate_pdf_receipt(
            cart_items,
            subtotal,
            telegram_id,
            customer_name
        )

        await query.message.reply_text(
            f"✅ Thank you {customer_name}! Your receipt is ready."
        )

        with open(pdf_path, "rb") as file:
            await query.message.reply_document(file)

    except Exception as e:
        print(f"Error generating receipt: {e}")
        await query.message.reply_text("✅ Order placed! (But receipt generation failed)")

    # STEP 4: Clear temporary cart
    clear_temp_cart(telegram_id)

    # STEP 5: Send New Ordering button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 New Ordering", callback_data="continue")]
    ])

    await query.message.reply_text(
        "Would you like to order another food?",
        reply_markup=keyboard
    )