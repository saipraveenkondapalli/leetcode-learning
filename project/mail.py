from project import app, mail
from flask import url_for
from project.models import User
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer as Serializer



def forget_password_mail_async(email):
    msg = Message()
    msg.subject = 'Reset Password'
    msg.recipients = [email]
    token = User.get_token(email)
    msg.sender = "App Password Reset"
    msg.body = f""" This is a link to reset your password: {url_for('reset_password', token=token, _external=True)} \nThis link  is valid only for 10 minutes.
    This is a system generated email. Please do not reply to this email."""
    mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)