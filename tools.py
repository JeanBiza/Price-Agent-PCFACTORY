import random
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
email_password = os.getenv("EMAIL_PASSWORD")
email_sender = os.getenv("EMAIL_SENDER")

def sent_random_code(email):
    code = random.randint(100000, 999999)

    subject = f'Confirmar email, Price agent'
    body = f"Tu codigo de validacion es: \n {code}"


    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_sender, email_password)
            server.send_message(msg)
        print('Se envio el correo')
    except Exception as e:
        print(f'Error: {e}')

    return code
