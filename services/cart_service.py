# Temporary
temp_carts = {}  
def add_to_temp_cart(telegram_id, item):
    if telegram_id not in temp_carts:
        temp_carts[telegram_id] = []
    
    for i in temp_carts[telegram_id]:
        if i['id'] == item['id']:
            i['quantity'] += 1
            return
    
    temp_carts[telegram_id].append({**item, 'quantity': 1})

def get_temp_cart(telegram_id):
    return temp_carts.get(telegram_id, [])

def remove_from_temp_cart(telegram_id, item_id):
    if telegram_id in temp_carts:
        temp_carts[telegram_id] = [i for i in temp_carts[telegram_id] if i['id'] != item_id]

def clear_temp_cart(telegram_id):
    temp_carts.pop(telegram_id, None)