from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from ..user import User
from ..models import Model as DBHelper
from . import bp
from app import login_manager
from .utils import PasswordHelper

DB = DBHelper()
PH = PasswordHelper()

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@bp.route('/register', methods=('POST',))
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('main.home'))
    if DB.get_user(email):
        return redirect(url_for('main.home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    print(DB.MOCK_USERS)
    return redirect(url_for('main.home'))


@bp.route("/login", methods=("POST",))
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = DB.get_user(email)
    if user and PH.validate_password(password, user['salt'], user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('main.account'))
    return render_template('home.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

