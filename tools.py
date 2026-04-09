import random
import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
email_sender = os.getenv("EMAIL_SENDER")

def sent_random_code(email):
    code = random.randint(100000, 999999)

    params = {
        "from": "Price Agent <onboarding@resend.dev>",
        "to": [email],
        "subject": "Confirmar email - Price Agent",
        "text": f"Tu código de verificación es: {code}"
    }

    try:
        resend.Emails.send(params)
        print("Email enviado")
    except Exception as e:
        print(f"Error: {e}")

    return code