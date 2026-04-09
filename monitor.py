from scraper import get_product_from_url
from database import get_active_products, init_db, get_last_price, save_price, get_users
from notifier import send_email_alert, send_telegram_alert

def run_monitor():
    init_db()
    users = get_users()
    for i in users:
        user_id = i[0]
        user_email = i[1]
        user_chat_id = i[3]
        products = get_active_products(user_id)
        if not products:
            print("No hay productos activos")
            continue
        for product in products:
            result = get_product_from_url(product[1])
            if result is None:
                print(f'No se pudo obtener el precio de {product[2]}, saltando...')
                continue
            name, price, image_url = result
            last_price = get_last_price(product[1], user_id)
            if last_price:
                if price != last_price:
                    send_telegram_alert(name , price, last_price, product[1], image_url, user_chat_id)
                    send_email_alert(name, price, last_price, product[1], user_email, image_url)
            save_price(product[1], product[2], price, user_id)

