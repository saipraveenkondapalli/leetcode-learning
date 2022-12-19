import time

from flask import request, render_template, redirect, url_for, make_response
from project.models import User
from project import app, oauth
from mongoengine.errors import NotUniqueError as MongoNotUniqueError
from flask_login import login_required, login_user, logout_user, current_user
import boto3
import random


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! <a href ="/login"> login </a> <a href = "/register"> register </a>'


@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        user = User.objects(email=email).first()
        if user:
            if user.social:
                return make_response("You already have an account. Please login with your social account", 401)
        if user is not None and user.check_password(password):
            login_user(user)
            return make_response("Login Successful", 200)
        else:
            return make_response("Wrong Email id or Password", 401)

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# ----------------------------------------------------Google Login--------------------------------------------------------
@app.route('/google', methods = ["POST", "GET"])
def google():
    google = oauth.create_client('google')
    redirect_url = url_for('authorize', _external= True)
    return google.authorize_redirect(redirect_url)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    email = user_info['email']
    user = User.objects(email=email).first()
    if not user:
        user = User()
        user.email = email
        user.name = user_info['name']
        user.social = True
        user.social_id = 'google'
        user.save()
    login_user(user)
    return redirect('/dashboard')

# ------------------------------------------------------- END OF GOOGLE LOGIN ----------------------------------------------------------------------------------



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user.name)



@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.confirm_password = request.form['cpassword']
        user.social = False
        user.save()
        login_user(user)
        return redirect('/dashboard')

    return render_template('register.html')



"""
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # generate a random file name using random module
        
        file.filename = str(random.randint(100000, 9999999999)) +'.'+ file.filename.split('.')[-1] # 1234567.jpg
        s3 = boto3.resource('s3', aws_access_key_id='73234ac2e5a5a497e7249fc13ab802e4',
                            aws_secret_access_key='e671453794d1b58b01d7c05bfa8f1345f28ad01d372b0685a6414b8c1a6acfc2',
                            endpoint_url='https://4e3989f550197dead69bd70821c5fc3f.r2.cloudflarestorage.com')

        bucket = s3.Bucket('leetcode-problems')
        bucket.upload_fileobj(file, file.filename)

        return "File uploaded Successfully"
    return render_template('upload.html')
    
"""
