import random
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()
email_password = os.getenv("EMAIL_PASSWORD")
email_sender = os.getenv("EMAIL_SENDER")

def sent_random_code(email):
    code = random.randint(100000, 999999)

    msg = MIMEMultipart('related')
    msg['Subject'] = "Confirmar email - Price Agent"
    msg['From'] = email_sender
    msg['To'] = email
    msg.attach(MIMEText(f"Tu código de verificación es: {code}", 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
        print("Email enviado")
    except Exception as e:
        print(f"Error: {e}")

    return code