from celery import Celery
from dotenv import load_dotenv
import os, smtplib, ssl

load_dotenv()

celery = Celery(
        'tasks',
        broker='pyamqp://guest@localhost//',
        backend="rpc://")

@celery.task
def send_email_task(email):
    context = ssl.create_default_context()

    sender_email = os.getenv("sender")
    password = os.getenv("email_pass")
    receiver_email = email

    message = """\
            Subject: Hi there

            This message is sent from @mustafaKane's HNG stage 3 messaging app."""

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return f"Email sent to {receiver_email}"
    except Exception as e:
        return f"Failed to send email to {receiver_email}: {e}"
