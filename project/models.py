from project import db,app, bcrypt
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
import random
import string

class User(UserMixin, db.Document):
    name = db.StringField(required= True)
    email = db.EmailField(unique=True, required = True)
    password = db.StringField()
    social = db.BooleanField(default=False)
    social_id = db.StringField()
    meta = {'collection': 'users'}

    @staticmethod
    def get_token(email):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps(email, salt='password-reset')

    @staticmethod
    def generate_password():
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash


@app.login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class Company(db.EmbeddedDocument):
    name = db.StringField(required=True)
    alias = db.StringField()
    freq = db.IntField()
    percentage = db.StringField()


class Code(db.EmbeddedDocument):
    language = db.StringField(required=True)
    code = db.StringField(required=True)


class Problems(db.Document):
    name = db.StringField(required=True)
    link_name = db.StringField()
    link = db.StringField(required=True)
    level = db.StringField()
    category = db.ListField(db.StringField())
    total_companies = db.IntField()
    company = db.EmbeddedDocumentListField(Company)
    code = db.EmbeddedDocumentListField(Code)
    meta = {'collection': 'problems'}
