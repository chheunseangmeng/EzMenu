# Temporary in-memory cart storage (not DB yet)
temp_carts = {}  # { telegram_id: [ {id, name, price, quantity, image_url} ] }

def add_to_temp_cart(telegram_id, item):
    if telegram_id not in temp_carts:
        temp_carts[telegram_id] = []
    
    # Check if item already in cart, increase quantity
    for i in temp_carts[telegram_id]:
        if i['id'] == item['id']:
            i['quantity'] += 1
            return
    # Add new item
    temp_carts[telegram_id].append({**item, 'quantity': 1})

def get_temp_cart(telegram_id):
    return temp_carts.get(telegram_id, [])

def remove_from_temp_cart(telegram_id, item_id):
    if telegram_id in temp_carts:
        temp_carts[telegram_id] = [i for i in temp_carts[telegram_id] if i['id'] != item_id]

def clear_temp_cart(telegram_id):
    temp_carts.pop(telegram_id, None)