import requests
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

load_dotenv()
TOKEN = os.getenv("TOKEN")
email_password = os.getenv("EMAIL_PASSWORD")
email_sender = os.getenv("EMAIL_SENDER")

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
    subject = f'Alerta de precio para {product_name}'
    body = _build_message(product_name, current_price, previous_price, url)


    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = receiver_email

    msg.attach(MIMEText(body, 'plain'))

    try:
        response_image = requests.get(url_image, headers={'User-Agent': 'Mozilla/5.0'})
        response_image.raise_for_status()
        image_mime = MIMEImage(response_image.content)
        msg.attach(image_mime)
    except Exception as e:
        print(f'No se pudo adjuntar la imagen: {e}')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_sender, email_password)
            server.send_message(msg)
        print('Se envio el correo')
    except Exception as e:
        print(f'Error: {e}')