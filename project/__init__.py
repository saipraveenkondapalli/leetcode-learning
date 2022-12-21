import os
from flask import Flask, request, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '<---YOUR_SECRET_FORM_KEY--->'


# --------------------------------------------FLASK Bcrypt CONFIGURATION -----------------------------------------------

bcrypt = Bcrypt(app)

# ------------------------------------------- GOOGLE OAuth Configuration -----------------------------------------------

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id = "562099229259-re04rb8ks9jvsfov6d9okag9orromgsn.apps.googleusercontent.com",
    client_secret="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",
    access_token_url="https://www.googleapis.com/oauth2/v4/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v3/",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url=f'https://accounts.google.com/.well-known/openid-configuration' )

# ----------------------------------------------- END OF GOOGLE OAuth --------------------------------------------

# ----------------------------------------------- MongoDB Configuration ------------------------------------------

app.config['MONGODB_SETTINGS'] = {
    'db': 'flask',
    'host': os.environ.get('MongoDB')
}

db = MongoEngine(app)

# ------------------------------------------- End of MongoDB -----------------------------------------------------

# ------------------------------------------- Login Manager Configuration ----------------------------------------

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------------------------------- End of Login Manager -----------------------------------------------

# ------------------------------------------- MAIL CONFIGURATION ---------------------------------------------------

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') # 'smtp.googlemail.com'
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') #

app.config['MAIL_USERNAME'] = os.environ.get('FLASK_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get("FLASK_MAIL_PASSWORD")
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

# ------------------------------------------- END OF MAIL CONFIGURATION --------------------------------------------

