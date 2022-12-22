import os
from flask import Flask, request, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# --------------------------------------------FLASK Bcrypt CONFIGURATION -----------------------------------------------

bcrypt = Bcrypt(app)

# ------------------------------------------- GOOGLE OAuth Configuration -----------------------------------------------

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id = os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret= os.environ.get('GOOGLE_CLIENT_SECRET'),
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


