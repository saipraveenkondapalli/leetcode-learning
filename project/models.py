from project import db,app
from flask_login import UserMixin


class User(UserMixin, db.Document):
    name = db.StringField(required= True)
    email = db.EmailField(unique=True, required = True)
    password = db.StringField()
    social = db.BooleanField(default=False)
    social_id = db.StringField()
    meta = {'collection': 'users'}

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

@app.login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class Category(db.EmbeddedDocument):
    cat = db.StringField()


class Problems(db.Document):
    name = db.StringField()
    link = db.StringField()
    level = db.StringField()
    category = db.EmbeddedDocumentListField(Category)

    meta = {'collection': 'problems'}
