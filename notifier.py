import requests
from dotenv import load_dotenv
import os
import smtplib
import resend

load_dotenv()
TOKEN = os.getenv("TOKEN")
resend.api_key = os.getenv("RESEND_API_KEY")

def _build_message(product_name: str, current_price: float, previous_price: float, url: str) -> str:
    msg = ""
    p = ""
    previous_price = int(previous_price)
    current_price = int(current_price)
    if current_price > previous_price:
        p = "subió"
    elif current_price < previous_price:
        p = "bajó"
    else:
        p = "se mantuvo"
    current_price = f"${current_price:,}".replace(",", ".")
    previous_price = f"${previous_price:,}".replace(",", ".")

    if p == "bajó" or p == "subió":
        msg = (
            f"🚨 Alerta de precio!\n"
            f"{product_name} {p} a {current_price}\n"
            f"Precio anterior: {previous_price}\n"
            f"🔗 {url}"
        )
    else:
        msg = (
            f"🚨 Alerta de precio!\n"
            f"{product_name} {p} en {current_price}\n"
            f"🔗 {url}"
        )

    return msg

def send_telegram_alert(product_name: str, current_price: float, previous_price: float, url: str, url_image: str, chat_id) -> None:
    if chat_id:
        url_msg = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
        caption = _build_message(product_name, current_price, previous_price, url)
        data = {
            "chat_id": chat_id,
            "photo" : url_image,
            "caption": caption
        }
        try:
            response = requests.post(url_msg, json=data)
            print(response.status_code)
        except Exception as e:
            print(f'ERROR: {e}')


def send_email_alert(product_name: str, current_price: float, previous_price: float, url: str, receiver_email: str, url_image: str) -> None:
    body = _build_message(product_name, current_price, previous_price, url)

    params = {
        "from": "Price Agent <onboarding@resend.dev>",
        "to": [receiver_email],
        "subject": f"Alerta de precio para {product_name}",
        "text": body
    }

    try:
        resend.Emails.send(params)
        print("Email enviado")
    except Exception as e:
        print(f"Error: {e}")