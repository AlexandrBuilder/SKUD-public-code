from flask_mail import Message

from app import mail


def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    mail.send(msg)
