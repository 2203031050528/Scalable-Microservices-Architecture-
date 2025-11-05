from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME="apikey",  # Must literally be "apikey"
    MAIL_PASSWORD=os.getenv("SENDGRID_API_KEY"),  # From .env
    MAIL_FROM=os.getenv("MAIL_FROM", "no-reply@yourdomain.com"),  # Verified sender
    MAIL_PORT=587,
    MAIL_SERVER="smtp.sendgrid.net",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)

async def send_email(recipient: str, subject: str, body: str, html: bool = True):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="html" if html else "plain"
    )
    await fm.send_message(message)
    return {"status": "Email sent", "to": recipient}
