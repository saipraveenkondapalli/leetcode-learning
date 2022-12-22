from project import app , bcrypt , db , login_manager , mail, oauth
from flask import render_template , redirect , url_for , flash , request, make_response
from project.models import User
from flask_login import login_user , logout_user , current_user , login_required
from mongoengine.errors import NotUniqueError as MongoNotUniqueError
from project.mail import forget_password_mail_async as forget_send_mail
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature


@app.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.objects(email=email).first()
        if user:
            if user.social:
                return make_response("You already have an account. Please login with your social account", 401)
        if user is not None and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            if not next:
                next = '/companies'
            return make_response(str(next), 200)
        else:
            return make_response("Wrong Email id or Password", 401)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['cpassword']
        if password == confirm_password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.social = False
        try:
            user.save()
            login_user(user)
            return make_response("Registration Successful", 200)
        except MongoNotUniqueError:
            return make_response("Email already exists", 401)
    return render_template('register.html')


# ----------------------------------------------------------- GOOGLE LOGIN --------------------------------------------------------
@app.route('/google', methods=["POST", "GET"])
def google():
    google = oauth.create_client('google')
    redirect_url = url_for('authorize', _external=True)
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
    return redirect('/companies')

# ------------------------------------------------------- END OF GOOGLE LOGIN ----------------------------------------------------------------------------------


@app.route('/forget', methods=['POST', 'GET'])
def forget():
    if request.method == "POST":
        email = request.form['email']
        user = User.objects(email=email).first()
        if user and not user.social:
            forget_send_mail(email)
            return make_response("Email sent", 200)
        elif user and user.social:
            return make_response("You have already registered with Google", 401)
        else:
            return make_response("No user associated with this email", 401)
    return render_template('forget.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = Serializer(app.config['SECRET_KEY'])  # creates a serializer object
    try:
        email = s.loads(token, salt='password-reset', max_age=600) # max age is 10 minutes   i.e 600 seconds
        user = User.objects(email=email).first()
        if request.method == 'POST':
                password_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
                user.password = password_hash
                user.save()
                return redirect('/login')


    except SignatureExpired:   # if the token is expired
        return render_template("forget.html", msg = "The token is expired")

    except BadSignature:   # if the token is invalid
        return render_template("forget.html", msg = "The token is invalid")

    return render_template('reset.html', username=user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

