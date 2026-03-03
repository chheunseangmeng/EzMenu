# services/menu_service.py
from database.db import get_connection

def get_menu_items(category=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if category and category != "all":
        cursor.execute("SELECT * FROM menu_items WHERE category=%s", (category,))
    else:
        cursor.execute("SELECT * FROM menu_items")

    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items