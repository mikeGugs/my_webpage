from flask import current_app
from flask_mail import Message
from threading import Thread
from .extensions import mail

def send_async_email(msg, app):
    with app.app_context():
        mail.send(msg)

def send_me_email(from_email, msg_subject, message):
    app = current_app._get_current_object()
    msg = Message(sender=app.config['MAIL_SENDER'],
                  recipients=[app.config['RECIPIENT_EMAIL']],
                  body=message,
                  subject=msg_subject
                  )
    thr = Thread(target=send_async_email, args=[msg, app])
    thr.start()
    return thr


