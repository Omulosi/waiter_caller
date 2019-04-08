from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from ..user import User
from . import bp
from app import login_manager
from .utils import PasswordHelper
from .forms import RegistrationForm, LoginForm
from config import Config

if Config.TEST:
    from ..mock_models import Model as DBHelper
else:
    from ..models import Model as DBHelper


DB = DBHelper()
PH = PasswordHelper()

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@bp.route('/register', methods=('POST','GET'))
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template("home.html", registrationform=form, loginform=LoginForm(),
                           onloadmessage="Registration successful. Please log in.")
    return render_template("home.html", registrationform=form, loginform=LoginForm())


@bp.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data,
            stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('main.account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form,
    registrationform=RegistrationForm())

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

