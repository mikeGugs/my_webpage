from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

def send_async_email(app, msg, mail_instance):
    with app.app_context():
        mail_instance.send(msg)


def send_me_email(subject, from_email, message, mail_instance):
    body = f"Email from: {from_email}\n\n{message}"
    app = current_app._get_current_object()
    print(app)
    msg = Message(body,
                  sender=app.config['MAIL_SENDER'],
                  recipients=app.config['RECIPIENT_EMAIL'])
    msg.body = body
    thr = Thread(target=send_async_email, args=[app, msg, mail_instance])
    thr.start()
    return thr
